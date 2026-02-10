# main.py
# -----------------------------------------------------------------------------
# Projet     : Système de Recommandation de Produits (Sujet 7)
# Module     : main.py
# Description:
#   Point d'entrée de l'application (Console).
#   Gère le menu principal, les interactions utilisateur et l'affichage des résultats.
# -----------------------------------------------------------------------------

import sys
from graphe import GrapheBiparti
from recommandation import MoteurRecommandation
# Importation des fonctions de gestion de données (I/O)
from gestion_donnees import charger_donnees, exporter_graphviz, ouvrir_graphviz_web

def afficher_entete():
    """Affiche une bannière textuelle pour le titre de l'application."""
    print("\n" + "="*60)
    print("   SYSTEME DE RECOMMANDATION - GRAPHE BIPARTI")
    print("   Algorithme de Filtrage Collaboratif (Jaccard)")
    print("="*60)

def afficher_menu():
    """Affiche les options disponibles dans le menu principal."""
    print("\n--- MENU PRINCIPAL ---")
    print("1. [Initialisation] Charger les données (donnees.txt)")
    print("2. [Analyse]        Afficher les statistiques du graphe")
    print("3. [Visualisation]  Voir le graphe (Navigateur Web)")
    print("4. [Traitement]     Lancer une Recommandation (Analyse complète)")
    print("5. [Export]         Sauvegarder le graphe (.dot)")
    print("0. [Sortie]         Quitter le programme")
    print("-" * 30)

def afficher_liste_utilisateurs(graphe):
    """
    Affiche la liste des utilisateurs existants dans le graphe.
    Cela aide l'opérateur à choisir un ID valide.
    Retourne False si le graphe est vide.
    """
    if not graphe.utilisateurs:
        print("\n[!] AVERTISSEMENT : La base de données est vide.")
        print("    Veuillez charger les données (Option 1) avant de continuer.")
        return False
    
    print("\n--- Liste des Utilisateurs disponibles ---")
    print(f"{'ID':<5} | {'Nom':<20} | {'Nb Achats'}")
    print("-" * 40)
    
    for u in graphe.utilisateurs.values():
        print(f"{u.id:<5} | {u.nom:<20} | {len(u.achats)}")
    print("-" * 40)
    return True

def main():
    """
    Boucle principale du programme.
    """
    # Instanciation des objets principaux
    graphe = GrapheBiparti()
    moteur = MoteurRecommandation(graphe)
    nom_fichier = "donnees.txt"

    afficher_entete()

    while True:
        afficher_menu()
        choix = input(">>> Entrez votre choix : ")

        # --- OPTION 1 : Chargement des données ---
        if choix == "1":
            print(f"\n[INFO] Lecture du fichier '{nom_fichier}' en cours...")
            charger_donnees(nom_fichier, graphe)

        # --- OPTION 2 : Statistiques ---
        elif choix == "2":
            print("\n--- Statistiques du Réseau ---")
            print(f" > Nombre d'Utilisateurs : {len(graphe.utilisateurs)}")
            print(f" > Nombre de Produits    : {len(graphe.produits)}")
            # On pourrait ajouter ici le nombre total d'arêtes (achats)
            nb_achats = sum(len(u.achats) for u in graphe.utilisateurs.values())
            print(f" > Total des Achats      : {nb_achats}")

        # --- OPTION 3 : Visualisation Web (Graphviz) ---
        elif choix == "3":
            if not graphe.utilisateurs:
                print("[!] Le graphe est vide.")
            else:
                # Ouvre le navigateur par défaut avec le diagramme
                ouvrir_graphviz_web(graphe)

        # --- OPTION 4 : Cœur du projet (Recommandation) ---
        elif choix == "4":
            # 1. On affiche d'abord la liste pour guider l'utilisateur
            if afficher_liste_utilisateurs(graphe):
                try:
                    id_input = input(">>> Entrez l'ID de l'utilisateur cible : ")
                    id_user = int(id_input)
                    
                    # Vérification si l'utilisateur existe
                    user_cible = graphe.utilisateurs.get(id_user)
                    
                    if user_cible:
                        print(f"\n[ANALYSE] Traitement pour : {user_cible.nom}")
                        
                        # Étape A : Trouver les voisins (Explication de la logique)
                        voisins = moteur.trouver_voisins_proches(id_user, k=3)
                        print(" > Voisins les plus proches (Basé sur Jaccard) :")
                        if not voisins:
                            print("   (Aucun voisin similaire trouvé)")
                        else:
                            for v, score in voisins:
                                print(f"   - {v.nom} (Similarité : {score:.2f})")

                        # Étape B : Générer les produits
                        recommandations = moteur.generer_recommandations(id_user)
                        
                        print("\n > RÉSULTAT : Produits Recommandés")
                        if not recommandations:
                            print("   [INFO] Aucune recommandation pertinente trouvée.")
                        else:
                            for produit, score in recommandations:
                                # Affichage propre
                                print(f"   * {produit.nom:<25} (Score de confiance : {score:.2f})")
                    else:
                        print(f"[ERREUR] L'ID {id_user} n'existe pas dans le graphe.")
                        
                except ValueError:
                    print("[ERREUR] Veuillez entrer un nombre entier valide.")

        # --- OPTION 5 : Export fichier ---
        elif choix == "5":
            exporter_graphviz(graphe)

        # --- OPTION 0 : Quitter ---
        elif choix == "0":
            print("\n[INFO] Arrêt du programme. Au revoir.")
            break

        else:
            print("\n[ERREUR] Choix invalide. Veuillez réessayer.")

'''
C'est une convention standard en Python. 
Elle signifie : 'Si ce fichier est exécuté directement (via la commande python main.py), 
alors la fonction main() doit être lancée. 
En revanche, si ce fichier est importé en tant que module par un autre script, 
aucune fonction ne doit s'exécuter automatiquement'.
'''
if __name__ == "__main__":
    main()