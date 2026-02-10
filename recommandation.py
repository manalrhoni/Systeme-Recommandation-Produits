# recommandation.py
# -----------------------------------------------------------------------------
# Projet     : Système de Recommandation de Produits (Sujet 7)
# Module     : recommandation.py
# Description:
#   Cœur algorithmique du projet.
#   Implémente le filtrage collaboratif "User-Based" en utilisant
#   la métrique de similarité de Jaccard.
# -----------------------------------------------------------------------------

from models import Utilisateur, Produit

class MoteurRecommandation:
    """
    Classe responsable du calcul des similarités et de la génération des suggestions.
    Elle traverse le graphe pour trouver des modèles (patterns) d'achat communs.
    """

    def __init__(self, graphe):
        """
        Initialise le moteur de recommandation.
        
        Args:
            graphe (GrapheBiparti): L'instance du graphe contenant les données.
        """
        self.graphe = graphe

    def calculer_similarite_jaccard(self, user_a, user_b):
        """
        Calcule l'indice de Jaccard entre deux utilisateurs A et B.
        
        Formule Mathématique :
            J(A, B) = |Intersection(A, B)| / |Union(A, B)|
            
        Explication :
            - Intersection : Produits achetés par les DEUX utilisateurs.
            - Union : Totalité des produits achetés par A ou B (sans doublons).
            
        Args:
            user_a (Utilisateur): Premier utilisateur.
            user_b (Utilisateur): Deuxième utilisateur.
            
        Returns:
            float: Score entre 0.0 (Aucun point commun) et 1.0 (Identiques).
        """
        achats_a = user_a.achats
        achats_b = user_b.achats

        # 1. Calcul de l'intersection (Produits communs)
        ensemble_commun = achats_a.intersection(achats_b)
        
        # 2. Calcul de l'union (Tous les produits uniques)
        ensemble_total = achats_a.union(achats_b)

        # Protection contre la division par zéro (si aucun achat)
        if len(ensemble_total) == 0:
            return 0.0

        # Calcul du coefficient
        score = len(ensemble_commun) / len(ensemble_total)
        return score

    def trouver_voisins_proches(self, id_target_user: int, k=3):
        """
        Identifie les 'k' utilisateurs les plus similaires à l'utilisateur cible
        (k-Nearest Neighbors).

        Algorithme :
            1. Parcourir tous les utilisateurs du graphe.
            2. Calculer le score Jaccard avec l'utilisateur cible.
            3. Trier les résultats par score décroissant.
            4. Retourner les k meilleurs.

        Args:
            id_target_user (int): ID de l'utilisateur à analyser.
            k (int): Nombre de voisins à retourner (défaut=3).

        Returns:
            list: Liste de tuples (Utilisateur, Score).
        """
        target_user = self.graphe.get_user(id_target_user)
        
        if not target_user:
            # Si l'utilisateur n'existe pas, on retourne une liste vide
            return []

        candidats = []

        # Parcours de tous les nœuds utilisateurs du graphe
        for autre_id, autre_user in self.graphe.utilisateurs.items():
            # On ne compare pas l'utilisateur avec lui-même
            if autre_id == id_target_user:
                continue
            
            # Calcul de la similarité
            score = self.calculer_similarite_jaccard(target_user, autre_user)
            
            # Filtrage : On ne garde que ceux qui ont au moins une similarité minimale
            if score > 0:
                candidats.append((autre_user, score))

        # Tri des candidats : Score le plus élevé en premier (Ordre décroissant)
        candidats.sort(key=lambda x: x[1], reverse=True)

        # On retourne les 'k' premiers éléments (Slicing)
        return candidats[:k]

    def generer_recommandations(self, id_target_user: int):
        """
        Génère une liste de produits recommandés pour un utilisateur donné.
        
        Principe :
            "Dis-moi qui sont tes voisins, je te dirai ce que tu devrais acheter."
            On regarde les produits achetés par les voisins proches que l'utilisateur
            n'a pas encore achetés lui-même.

        Args:
            id_target_user (int): ID de l'utilisateur cible.

        Returns:
            list: Liste de tuples (Produit, Score_Confiance) triée.
        """
        target_user = self.graphe.get_user(id_target_user)
        if not target_user:
            return []

        # Étape 1 : Identifier le voisinage (Top 3 voisins)
        voisins = self.trouver_voisins_proches(id_target_user, k=3)
        
        # Dictionnaire pour accumuler les scores des produits potentiels
        # Structure : {ObjetProduit: Score_Cumulé}
        suggestions = {}

        # Étape 2 : Agrégation des produits des voisins
        for voisin, score_similarite in voisins:
            for produit in voisin.achats:
                # Filtrage : L'utilisateur a-t-il DÉJÀ acheté ce produit ?
                if produit in target_user.achats:
                    continue
                
                # Pondération : Plus le voisin est similaire, plus sa recommandation compte
                if produit not in suggestions:
                    suggestions[produit] = 0
                
                suggestions[produit] += score_similarite

        # Étape 3 : Finalisation et Tri
        # On transforme le dictionnaire en liste de tuples et on trie par score
        resultats = sorted(suggestions.items(), key=lambda x: x[1], reverse=True)
        
        return resultats