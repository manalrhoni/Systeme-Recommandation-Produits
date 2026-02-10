=============================================================================
PROJET 7 : SYSTÈME DE RECOMMANDATION DE PRODUITS (FILTRAGE COLLABORATIF)
Module   : Structures de Données Avancées et Théorie des Graphes
Encadré par : Pr. Ouafae Baida
Lieu     : Faculté des Sciences et Techniques de Tanger (FSTT)
Date     : Janvier 2026
=============================================================================

1. ÉQUIPE DE RÉALISATION
------------------------
Ce projet a été conçu et développé par :
* Manal Rhoni Aref
* Souhaila Benaouate
* Meryem El Khoumri
* Moad Afylal
* Sofyane Fritit

2. DESCRIPTION DU PROJET
------------------------
Ce projet implémente un moteur de recommandation inspiré des systèmes utilisés 
par les géants du e-commerce (ex: Amazon). L'objectif est de suggérer des 
produits pertinents à un utilisateur en analysant son historique d'achats 
et en le comparant à celui des autres utilisateurs.

Le cœur du système repose sur la modélisation des données sous forme de 
Graphe Biparti (Utilisateurs <-> Produits) et l'utilisation de l'indice 
de similarité de Jaccard pour identifier les voisinages (k-Nearest Neighbors).

3. ARCHITECTURE TECHNIQUE (FICHIERS)
------------------------------------
Le code source est structuré de manière modulaire pour garantir la lisibilité 
et la maintenance :

* main.py             : Point d'entrée de l'application. Gère le menu interactif.
* models.py           : Définit les entités du graphe (Classes Utilisateur et Produit).
* graphe.py           : Structure de données du Graphe Biparti (Tables de hachage).
* recommandation.py   : Logique algorithmique (Calcul Jaccard, Tri, Filtrage).
* gestion_donnees.py  : Gestion des Entrées/Sorties (Lecture fichier & Export Graphviz).
* donnees.txt         : Base de données textuelle contenant l'historique des achats.

4. PRÉREQUIS ET INSTALLATION
----------------------------
* Langage : Python 3.x (Version 3.8 ou supérieure recommandée).
* Bibliothèques : Aucune installation externe n'est requise. Le projet utilise 
  uniquement les modules standards de Python (sys, webbrowser, urllib).

5. INSTRUCTIONS D'EXÉCUTION
---------------------------
Pour tester le projet et reproduire les résultats, suivez ces étapes :

Étape 1 : Lancement
   Ouvrez un terminal dans le dossier du projet et exécutez :
   $ python main.py

Étape 2 : Chargement des données
   Dans le menu, choisissez l'option [1]. Le système va lire le fichier 
   'donnees.txt' et construire le graphe en mémoire.

Étape 3 : Vérification (Facultatif)
   Choisissez l'option [2] pour afficher les statistiques (Nombre de nœuds/arêtes) 
   ou l'option [3] pour visualiser graphiquement le réseau dans votre navigateur.

Étape 4 : Génération de Recommandations
   Choisissez l'option [4] pour lancer l'algorithme.
   - Le système affichera la liste des utilisateurs disponibles.
   - Entrez l'ID d'un utilisateur cible (ex: 16, 18...).
   - Le système affichera ses voisins les plus proches puis les produits suggérés.

6. DÉTAILS DE L'IMPLÉMENTATION
------------------------------
* Modélisation : Nous avons utilisé un Graphe Biparti Non-Orienté où les arêtes 
  représentent exclusivement les relations d'achat.
* Stockage : Utilisation de dictionnaires Python pour garantir une complexité 
  d'accès aux nœuds en O(1).
* Similarité : L'indice de Jaccard a été choisi car il est particulièrement 
  adapté aux ensembles binaires (Achat / Pas d'achat).
  Formule : J(A,B) = |Achats_A ∩ Achats_B| / |Achats_A ∪ Achats_B|

7. SCÉNARIOS DE TEST (DÉMONSTRATION)
------------------------------------
Pour démontrer la pertinence des résultats, nous avons inclus des profils types 
dans le fichier 'donnees.txt' :

* Cas 1 : Profil "Gamer" (Testez l'ID 16 - Sofyane)
  -> Le système détecte une similarité avec Moad et Yassine.
  -> Recommandation attendue : Accessoires de jeu (Souris RGB, Chaise Gaming).

* Cas 2 : Profil "Professionnel" (Testez l'ID 18 - Manal)
  -> Le système détecte une similarité avec Ahmed et Karim.
  -> Recommandation attendue : Matériel de bureau (Webcam Pro, Clavier Silent).

=============================================================================