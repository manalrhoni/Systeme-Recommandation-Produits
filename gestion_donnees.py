# gestion_donnees.py
# -----------------------------------------------------------------------------
# Projet     : Système de Recommandation de Produits (Sujet 7)
# Module     : gestion_donnees.py
# Description:
#   Module responsable de la persistance et de la visualisation.
#   Gère le chargement des données depuis un fichier texte et l'exportation
#   vers le format DOT (Graphviz) pour la visualisation graphique.
# -----------------------------------------------------------------------------

import webbrowser
import urllib.parse
from graphe import GrapheBiparti

def charger_donnees(fichier, graphe):
    """
    Lit un fichier texte structuré et peuple le graphe biparti.

    Format du fichier attendu par ligne :
    ID_USER [Espace] NOM_USER [Espace] ID_PROD [Espace] NOM_PRODUIT
    Exemple : 1 Moad 101 PC_Portable

    Args:
        fichier (str): Chemin du fichier de données.
        graphe (GrapheBiparti): L'instance du graphe à remplir.
    """
    try:
        # Ouverture avec encodage UTF-8 pour gérer les accents éventuels
        with open(fichier, "r", encoding="utf-8") as f:
            lignes_traitees = 0
            
            for ligne in f:
                ligne = ligne.strip()
                # Ignorer les lignes vides
                if not ligne:
                    continue

                # Traitement de la chaîne de caractères :
                # On utilise split(None, 3) pour limiter le découpage aux 3 premiers espaces.
                # Cela permet au 'Nom du Produit' (le dernier élément) de contenir des espaces.
                # Ex: "102 Souris sans fil" -> ID=102, Nom="Souris sans fil"
                parts = ligne.split(None, 3)

                # Vérification de l'intégrité de la ligne
                if len(parts) < 4:
                    print(f"[AVERTISSEMENT] Format incorrect, ligne ignorée : {ligne}")
                    continue

                id_user, nom_user, id_prod, nom_prod = parts

                try:
                    # Conversion des identifiants en entiers
                    id_user_int = int(id_user)
                    id_prod_int = int(id_prod)
                except ValueError:
                    print(f"[ERREUR] Type de données invalide (entier attendu) : {ligne}")
                    continue

                # Construction du Graphe :
                # 1. Création (ou récupération) des nœuds
                graphe.ajouter_utilisateur(id_user_int, nom_user)
                graphe.ajouter_produit(id_prod_int, nom_prod)
                
                # 2. Création de l'arête (Relation d'achat)
                graphe.ajouter_achat(id_user_int, id_prod_int)
                lignes_traitees += 1

        print(f"[SUCCES] Chargement terminé. {lignes_traitees} relations importées.")

    except FileNotFoundError:
        print(f"[ERREUR CRITIQUE] Le fichier '{fichier}' est introuvable.")
    except Exception as e:
        print(f"[ERREUR] Une erreur inattendue est survenue : {e}")


def generer_dot_content(graphe):
    """
    Génère la description textuelle du graphe au format DOT (Graphviz).
    Cette représentation est utilisée pour l'export fichier et la visualisation web.

    Returns:
        str: Le code source du graphe en langage DOT.
    """
    dot_lines = []
    
    # Début du graphe
    dot_lines.append("graph GrapheBiparti {")
    
    # Orientation Gauche -> Droite (Left to Right) pour simuler un graphe biparti
    dot_lines.append("  rankdir=LR;")
    dot_lines.append("  node [fontname=\"Arial\"];")

    # 1. Définition des nœuds Utilisateurs (Ensemble U)
    # Style : Ellipse bleue
    for user in graphe.utilisateurs.values():
        dot_lines.append(f'  "U{user.id}" [label="{user.nom}", shape=ellipse, style=filled, fillcolor=lightblue, color=blue];')

    # 2. Définition des nœuds Produits (Ensemble V)
    # Style : Rectangle vert
    for prod in graphe.produits.values():
        dot_lines.append(f'  "P{prod.id}" [label="{prod.nom}", shape=box, style=filled, fillcolor=lightgreen, color=green];')

    # 3. Définition des Arêtes (Liens d'achat)
    for user in graphe.utilisateurs.values():
        for prod in user.achats:
            # Création du lien non-orienté (--)
            dot_lines.append(f'  "U{user.id}" -- "P{prod.id}";')

    dot_lines.append("}")
    return "\n".join(dot_lines)


def exporter_graphviz(graphe, fichier="graphe.dot"):
    """
    Sauvegarde la représentation DOT du graphe dans un fichier local.
    """
    try:
        content = generer_dot_content(graphe)
        with open(fichier, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[SUCCES] Graphe exporté dans le fichier '{fichier}'.")
    except Exception as e:
        print(f"[ERREUR] Echec de l'exportation : {e}")


def ouvrir_graphviz_web(graphe):
    """
    Automatise la visualisation du graphe.
    Génère le code DOT, l'encode en URL, et l'ouvre dans un service web externe.
    
    Cela évite d'avoir à installer le logiciel Graphviz en local pour la démonstration.
    """
    print("[TRAITEMENT] Génération du lien de visualisation...")
    
    try:
        # 1. Récupération du code DOT
        dot_content = generer_dot_content(graphe)
        
        # 2. Encodage URL (pour gérer les espaces, retours à la ligne, etc.)
        # Exemple : " " devient "%20"
        encoded_dot = urllib.parse.quote(dot_content)
        
        # 3. Construction de l'URL vers l'outil "Graphviz Online"
        url = f"https://dreampuf.github.io/GraphvizOnline/#{encoded_dot}"
        
        # 4. Ouverture du navigateur par défaut
        webbrowser.open(url)
        print("[SUCCES] Navigateur ouvert. Veuillez consulter la fenêtre graphique.")
        
    except Exception as e:
        print(f"[ERREUR] Impossible d'ouvrir le navigateur : {e}")