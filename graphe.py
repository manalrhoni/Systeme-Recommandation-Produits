# graphe.py
# -----------------------------------------------------------------------------
# Projet     : Système de Recommandation de Produits (Sujet 7)
# Module     : graphe.py
# Description:
#   Définit la classe principale GrapheBiparti.
#   Gère le stockage des nœuds (Utilisateurs/Produits) et la création
#   des arêtes (Relations d'achat).
# -----------------------------------------------------------------------------

from models import Utilisateur, Produit

class GrapheBiparti:
    """
    Structure de données représentant un Graphe Biparti Non-Orienté.
    
    Composants :
      - Ensemble U : Utilisateurs
      - Ensemble V : Produits
      - Arêtes E : Relations d'achat (u, v)
    
    Implémentation :
      Utilisation de tables de hachage (Dictionnaires Python) pour stocker
      les nœuds, garantissant un accès en temps constant O(1) par ID.
    """

    def __init__(self):
        """
        Constructeur du Graphe.
        Initialise les conteneurs de données vides.
        """
        # Dictionnaire : Clé = ID (int), Valeur = Objet Utilisateur
        self.utilisateurs = {}
        
        # Dictionnaire : Clé = ID (int), Valeur = Objet Produit
        self.produits = {}

    def ajouter_utilisateur(self, id_user: int, nom: str):
        """
        Ajoute un nœud Utilisateur au graphe s'il n'existe pas déjà.

        Args:
            id_user (int): L'identifiant unique.
            nom (str): Le nom de l'utilisateur.
        """
        if id_user not in self.utilisateurs:
            nouveau_user = Utilisateur(id_user, nom)
            self.utilisateurs[id_user] = nouveau_user
        
    def ajouter_produit(self, id_produit: int, nom: str):
        """
        Ajoute un nœud Produit au graphe s'il n'existe pas déjà.

        Args:
            id_produit (int): L'identifiant unique.
            nom (str): Le nom du produit.
        """
        if id_produit not in self.produits:
            nouveau_produit = Produit(id_produit, nom)
            self.produits[id_produit] = nouveau_produit

    def ajouter_achat(self, id_user: int, id_produit: int):
        """
        Crée une arête (lien) entre un utilisateur et un produit.
        Cette méthode matérialise la relation "A acheté" dans le graphe.

        Args:
            id_user (int): ID de l'acheteur.
            id_produit (int): ID du produit acheté.
        
        Note:
            Si l'un des ID n'existe pas, la relation est ignorée silencieusement
            pour ne pas interrompre le chargement de gros fichiers.
        """
        # Vérification de l'existence des nœuds avant de créer le lien
        if id_user in self.utilisateurs and id_produit in self.produits:
            
            user = self.utilisateurs[id_user]
            prod = self.produits[id_produit]

            # Création du lien bidirectionnel (Graphe non-orienté)
            # 1. L'utilisateur ajoute le produit à son historique
            user.achats.add(prod)
            
            # 2. Le produit ajoute l'utilisateur à sa liste d'acheteurs
            prod.acheteurs.add(user)

    def get_user(self, id_user: int):
        """
        Récupère un objet Utilisateur par son ID.
        
        Returns:
            Utilisateur: L'objet trouvé, ou None si inexistant.
        """
        return self.utilisateurs.get(id_user)

    def get_produit(self, id_produit: int):
        """
        Récupère un objet Produit par son ID.
        
        Returns:
            Produit: L'objet trouvé, ou None si inexistant.
        """
        return self.produits.get(id_produit)

    def afficher_statistiques(self):
        """
        Affiche un résumé textuel de l'état actuel du graphe.
        Utile pour le débogage ou l'aperçu rapide.
        """
        nb_users = len(self.utilisateurs)
        nb_prods = len(self.produits)
        # Calcul du nombre total d'arêtes (somme des degrés des utilisateurs)
        nb_relations = sum(len(u.achats) for u in self.utilisateurs.values())

        print(f"--- État du Graphe ---")
        print(f" Nœuds Utilisateurs : {nb_users}")
        print(f" Nœuds Produits     : {nb_prods}")
        print(f" Arêtes (Achats)    : {nb_relations}")
        print("-" * 22)