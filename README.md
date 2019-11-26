# DOCUMENTATION

- [DOCUMENTATION](#documentation)
      - [Groupe: PYTHON_03](#groupe-python03)
      - [Sujet : Application Web de séries](#sujet--application-web-de-s%c3%a9ries)
      - [Participants : KADIRI Hamza | BENAUW Edouard | QUESNEL Clement](#participants--kadiri-hamza--benauw-edouard--quesnel-clement)
  - [Guide d'installation](#guide-dinstallation)
  - [Manuel d'utilisation](#manuel-dutilisation)
  - [Fonctionnalités](#fonctionnalit%c3%a9s)
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

Une fois sur le terminal du serveur deux possibilités vous sont offertes:

1. Créer une base de donnée vierge en executant la commande suivante:

   `python db_creation.py`

2. Créer une base de donnée contenant un user avec quelques séries favorites:

   `python db_creation.py import`

Si vous choisissez la deuxième option l'utilisateur existant a pour attributs:

**username** : user_test
**email** : test@test.com
**password** : test

cependant avec cet utilisateur vous ne pourrez pas voir les notifications par mail

## Manuel d'utilisation

## Fonctionnalités

- Gestion d'utilisateur
- Recherche d'une série
- Ajout d'une série au favoris
- Notifications (sur l’application et par mails)
- Parcours des saisons et épisodes des séries favorites
- Gestion des exceptions

## Architecture et choix techniques

### Introduction

Nous avons choisi de réaliser le front-end en ReactJS qui communique avec le serveur grâce à une API developpee en Python avec la librairie flask. La gestion des donnees se fait en python grâce au fichier models.py qui utilise sqlalchemy afin de structurer les données selon les principes de programmation orientée objet et de les stocker dans une base de données postgresql.

### Client

Pour la partie client, nous nous sommes appuyés sur le framework [Material UI](https://material-ui.com/) pour les composants CSS.
Pour une gestion du flux de donnéés plus organisée, nous avons utilisé la librairie [Redux](https://redux.js.org/)

### Api 

L'API du serveur est conçue pour renvoyer des données au format JSON. Il s'agit d'une application Flask, dont le point d'entrée se situe dans app.py et la configuration dans config.py.

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
    Reçoit un user_id et une serie_id  et permet d'ajouter (ou d'enlever) une série aux favoris de l'utilisateur. Dans le cas de l'ajout aux favoris et si la série a un prochain épisode de prévu, une notification et un mail sont envoyés à l'utilisateur.

Pour tous les endpoint utilisant des inputs de l'utilisateur, ceux-ci sont préalablement vérifiés avec les fonctions situées dans form_validation.py.

L'application se base sur des données sur les séries récupérées via l'API de TMDB (https://developers.themoviedb.org/3/getting-started/introduction), qui sont récupérées via les fonctions situées dans tmdb_api.py.

### Gestion des exceptions

L'API gère un panel d'exceptions. Certaines sont des exceptions personnalisées, créées pour l'application. D'autres sont des exceptions standards, gérées nativement par Flask et appelées à l'aide de la fonction abort(error_code).

**Exceptions personnalisées :**

- **RequestExceptionOMDB :** l'exception est renvoyée en cas d'erreur lors d'une requête faite à l'API de TMDB.
 L'erreur la plus commune correspond à un dépassement de la limite de requêtes de l'API (40 requêtes toutes les 10 secondes) et une erreur 429 est renvoyée dans ce cas. Dans les autres cas, une erreur 500 est renvoyée.
 
- **InvalidAuth :** l'utilisateur a tenté de s'identifier avec un nom d'utilisateur ou un mot de passe erroné sur la route "/token". Une erreur 400 est renvoyée.

- **InvalidForm :** l'utilisateur a fait une requête POST comportant des données erronées. Une erreur 400 est renvoyée.

- **InvalidDBOperation :** une erreur est survenue lors d'une opération dans la BDD à cause d'une opération non authorisée. Une erreur 403 est renvoyée.

**Exceptions standard de Flask :**

- **400 : Bad Request.** Cette erreur est renvoyée en cas de requête erronée de l'utilisateur, dans les cas non prévus par InvalidAuth et InvalidForm.

- **401 : Unauthorized.** Cette erreur est renvoyée lorsque l'utilisateur envoie un token non valide (le client n'est pas autorisé à accéder à l'application)

- **403 : Forbidden.** Cette erreur est renvoyée lorsque l'utilisateur veut faire une opération interdite, typiquement accéder à une route correspondant aux informations d'un autre utilisateur.

- **404 : Not Found.** Cette erreur est renvoyée lorsque l'entité concernée par la requête (utilisateur, notification) n'est pas trouvée en BDD.

- **500 : Internal Error.** Cette erreur est l'erreur par défaut et correspond aux exceptions non prévues lors du développement de l'application.

### Modèle de données

### Stockage des données
