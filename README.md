# DOCUMENTATION

- [DOCUMENTATION](#documentation)
      - [Groupe: PYTHON_03](#groupe-python03)
      - [Sujet : Application Web de séries](#sujet--application-web-de-s%c3%a9ries)
      - [Participants : KADIRI Hamza | BENAUW Edouard | QUESNEL Clement](#participants--kadiri-hamza--benauw-edouard--quesnel-clement)
  - [Guide d'installation](#guide-dinstallation)
  - [Manuel d'utilisation](#manuel-dutilisation)
  - [Fonctionnalités :](#fonctionnalit%c3%a9s)
  - [Architecture et choix techniques](#architecture-et-choix-techniques)
    - [Introduction](#introduction)
    - [Client](#client)
    - [Api](#api)
    - [Gestion des exceptions](#gestion-des-exceptions)
    - [Modèle de données](#mod%c3%a8le-de-donn%c3%a9es)
    - [Stockage des données](#stockage-des-donn%c3%a9es)

#### Groupe: PYTHON_03

#### Sujet : Application Web de séries

#### Participants : KADIRI Hamza | BENAUW Edouard | QUESNEL Clement

## Guide d'installation

blabla

Une fois l'application lancée vous devez créer la base de donnée.
Pour cela, ouvrir un terminal dans le dossier de l'application et afin de rentrer dans le terminal du serveur exécuter la commande suivante :

`docker exec -it server sh`

Une fois sur le terminal du serveur il faut créer une base de donnée vierge en executant la commande suivante:

   `python db_creation.py`

## Manuel d'utilisation

Une fois l'application et la base de données créées, l'utilisateur peut découvrir l'application 
grâce à un navigateur web de son choix, en entrant l'adresse suivante:
localhost:3001.

Lors de la première utilisation l'utilisateur doit s'enregistrer grâce au bouton signup.
Une fois enregistré, il est redirigé vers la page d'accueil. Depuis cette page d'accueil l'utilisateur a 
plusieurs possibilités :
 - l'application lui proprose différentes séries du moment classées par genre.

 - il peut utiliser la barre de recherche lui permet de recherche sur l'ensemble des séries. Pour voir l'ensemble des détails,
il doit cliquer sur l'image de sa série puis "more details" pour accéder à la page détailée.

 - il peut consulter ses notifications (s'il possède des séries favorites en cours) en cliquant sur la petite cloche
 en haut à droite
 
 - il peut cliquer sur l'icon utilisateur en haut à droite pour:
   1. Se déconnecter grâce à Signup
   2. Consulter et parcourir les episodes de ses saisons favorites grâce au bouton favorites 


## Fonctionnalités de l'application:

- Gestion d'utilisateur
  1. Connexion
  2. Déconnexion
  3. Creation de compte
  4. Attribution d'un token d'identification
  5. Vérification de la validité du tokken
- Barre de recherche dynamique
- Gestion des séries favorites d'un utilisateur
  1. Ajout d'une ou plusieurs au favoris
  2. Suppression d'une ou plusieurs séries au favoris
  3. Création de notifications dans l'application pour prévenir des nouveaux épisodes à venir
  4. Création de notifications mail, à l'ajout d'une série et à chaque nouvel épisode sortie
- Parcours des saisons et épisodes des séries favorites
- Gestion des exceptions

## Architecture et choix techniques

### Introduction

Nous avons choisi de réaliser le front-end en ReactJS qui communique avec le serveur grâce à une API developpee en Python avec la librairie flask. La gestion des donnees se fait en python grâce au fichier models.py qui utilise sqlalchemy afin de structurer les données selon les principes de programmation orientée objet et de les stocker dans une base de données postgresql.

### Client

Pour la partie client, nous nous sommes appuyés sur le framework [Material UI](https://material-ui.com/) pour les composants CSS.
Pour une gestion du flux de données plus organisée, nous avons utilisé la librairie [Redux](https://redux.js.org/)

### Api 

L'API du serveur est conçue pour renvoyer des données au format JSON.

Elle se base sur une authentification de l'utilisateur à l'aide d'un système de token :

1. Lorsqu'un utilisateur se connecte sur l'application, celui-ci envoie au serveur son nom d'utilisateur et son mot de passe.
2. Si ceux-ci sont corrects, un token est renvoyé au client. Celui-ci est créé à partir de la classe TimedJSONWebSignatureSerializer de la librairie itsdangerous, de l'id de l'utilisateur, d'une durée de validité fixée (ici 10 minutes) et de la clé secrète du serveur.
3. Par la suite, lorsqu'un utilisateur veut utiliser une route nécessitant une authentification, celui envoie son token précédée de "Token" dans l'en-tête "Authorization" de sa requête HTTP. 
4. Le token est ensuite désérialisé à l'aide de la clé secrète du serveur afin de vérifier sa date d'expiration et d'obtenir l'id de l'utilisateur. 
Si le token est valide, on peut alors directement récupérer les droits d'accès de l'utilisateur dans la BDD à l'aide de l'id ainsi obtenue.

L'API comporte les endpoints suivants, correspondants aux fonctionnalités de l'application :

1. **Ping :**
    - **Endpoint :** *"/"*, **Méthode :** *GET*  
    Renvoie un statut "200 OK" si le serveur est en marche
   
2. **Authentification :**
    - **Endpoint :** *"/token"*, **Méthode :** *POST*   
    Reçoit une requête POST comportant un nom d'utilisateur et un mot de passe et renvoie un token si ceux-ci sont corrects
    
3. **Recherche d'informations sur les séries :**
    - **Endpoint :** *"/search"*, **Méthode :** *GET*  
    Reçoit une chaîne de caractères et renvoie toutes les séries dont le nom comporte cette chaîne de caractère
    - **Endpoint :** *"/discover"*, **Méthode :** *GET*  
    Renvoie des suggestions de série Sends series suggestions
    - **Endoint :** *"/series/<serie_id>"*, **Méthode :** *GET*  
    Renvoie des informations à propos de la série identifiée par serie_id Sends information about the serie identified by serie_id
    
4. **Ajout d'utilisateurs :**
    - **Endpoint :** *"/users"*, POST*  
    Reçoit un nom d'utilisateur, un mot de passe et une addresse mail et inscrit l'utilisateur dans la BDD si cela est possible
    
5. **Obtention d'informations sur un utilisateur :**
    - **Endpoint :** *"/users/<user_id>"*, **Méthode :** *GET*  
    Renvoie les informations de l'utilisateur identifié par user_id
    - **Endpoint :** *"/users/<user_id>/series"*, **Méthode :** *GET*  
    Renvoie les séries favorites de l'utilisateur identifié par user_id
    - **Endpoint :** *"/users/<user_id>/notifications"*, **Méthode :** *GET*  
    Renvoie les notifications de l'utilisateur identifié par user_id
    - **Endpoint :** *"/users/<user_id>/notifications"*, **Méthode :** *POST*  
    Reçoit une liste de notifications concernant l'utilisateur identifié par user_id et qui doivent être marquées comme lu, et effectue ces opérations en BDD si possible   
    
6. **Gestion des favoris :**
    - **Endpoint :** *"/favorite"*, **Méthode :** *GET*  
    Reçoit un user_id et une serie_id et renvoie une valeur "is_favorite" valant True si la série est dans les favoris de l'utilisateur
    - **Endpoint :** *"/favorite"*, **Méthode :** *POST*  
    Reçoit un user_id et une serie_id  et permet d'ajouter (ou d'enlever) une série aux favoris de l'utilisateur


### Gestion des exceptions

### Modèle de données

Les données sont organisées selon 8 grandes classes pythons:
 - Série
 - Saison
 - Episode
 - Notification
 - User
 - Personne
 - Actor
 - Productor

Pour avoir l'ensemble des détails sur le modèle de données, le diagramme UML est disponible
à la racine du dossier (all_models.uml)
 
### Stockage des données

Nous avons décidé d'utiliser une base de données postgressql dont la connexion se fait
par sql alchemy. 

La base de données est accessible grâce un adminer à l'adresse:
localhost:8080