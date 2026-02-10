# models.py
# -----------------------------------------------------------------------------
# Projet     : Système de Recommandation de Produits (Sujet 7)
# Module     : models.py
# Description:
#   Ce fichier contient les définitions des structures de données (Classes)
#   qui représentent les entités du Graphe Biparti.
#   Il définit les nœuds "Utilisateur" et les nœuds "Produit".
# -----------------------------------------------------------------------------

class Produit:
    """
    Cette classe représente un nœud de type 'Produit' dans le graphe biparti.
    Chaque instance correspond à un article unique disponible à l'achat.
    """

    def __init__(self, id_produit: int, nom: str):
        """
        Constructeur de la classe Produit.

        Args:
            id_produit (int): Identifiant unique du produit (ex: 101).
            nom (str): Désignation du produit (ex: "Clavier_Gamer").
        """
        self.id = id_produit
        self.nom = nom
        
        # Structure de données : Ensemble (Set)
        # Contient les références vers les objets Utilisateur ayant acheté ce produit.
        # L'utilisation d'un 'set' garantit l'unicité des relations (pas de doublons) 
        # (+ Garantit Un Bon  Calcul De Jaccard)
        # et permet une complexité de recherche en O(1).
        self.acheteurs = set() 

    def __repr__(self):
        """
        Représentation textuelle de l'objet pour le débogage et l'affichage.
        """
        return f"<Produit ID={self.id} Nom='{self.nom}'>"


class Utilisateur:
    """
    Cette classe représente un nœud de type 'Utilisateur' dans le graphe biparti.
    Chaque instance correspond à un client du système.
    """

    def __init__(self, id_user: int, nom: str):
        """
        Constructeur de la classe Utilisateur.

        Args:
            id_user (int): Identifiant unique de l'utilisateur (ex: 1).
            nom (str): Nom de l'utilisateur (ex: "Moad").
        """
        self.id = id_user
        self.nom = nom
        
        # Structure de données : Ensemble (Set)
        # Liste d'adjacence contenant les objets Produit achetés par cet utilisateur.
        # Liste d'adjacence : Qui sont vos voisins ? Les Produit Que L'utilisateur à acheter
        # Cela matérialise les arêtes du graphe entre l'utilisateur et les produits.
        self.achats = set()

    def __repr__(self):
        """
        Représentation textuelle de l'objet pour le débogage et l'affichage.
        """
        # ex : <Utilisateur ID=1 Nom='Moad'>
        return f"<Utilisateur ID={self.id} Nom='{self.nom}'>"