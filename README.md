# DOCUMENTATION

#### Groupe: PYTHON_03
#### Sujet : Application Web de séries
#### Participants : KADIRI Hamza | BENAUW Edouard | QUESNEL Clement

## Guide d'installation

blabla

Une fois l'application lancée vous devez créer la base de donnée. 
Pour cela, ouvrir un terminal dans le dossier de l'application et afin de rentrer dans le terminal du serveur exécuter la commande suivante :

```docker exec -it server sh```

Une fois sur le terminal du serveur deux possibilités vous sont offertes:
1) Créer une base de donnée vierge en executant la commande suivante:

    ```python db_creation.py```
 
2) Créer une base de donnée contenant un user avec quelques séries favorites:

    ```python db_creation.py import```

Si vous choisissez la deuxième option l'utilisateur existant a pour attributs:

**username** : user_test
**email** : test@test.com
**password** : test

cependant avec cet utilisateur vous ne pourrez pas voir les notifications par mail

## Manuel d'utilisation

## Fonctionnalités :
- Gestion d'utilisateur
- Recherche d'une série
- Ajout d'une série au favoris
- Notifications (sur l’application et par mails)
- Parcourt des saisons et épisodes des séries favorites
- gestion des exceptions

## Architecture et choix techniques
### Introduction
Nous avons choisi de réaliser le front-end en ReactJS qui communique avec le serveur grâce à une API developpee en Python avec la librairie flask. La gestion des donnees se fait en python grâce au fichier models.py qui utilise sqlalchemy afin de structurer les données selon les principes de programmation orientée objet et de les stocker dans une base de données postgresql.
### Client
### Api 
### Gestion des exceptions
### Modèle de données
### Stockage des données
