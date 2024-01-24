# Système de fichiers distribués.

## Organisation du répo Git

À la racine de ce repo, vous trouverez les dossiers "Code" et "Documents". Dans le premier, il y a tous
les fichiers concernant le code source de l'application et dans le second, il y a tous les documents d'analyse, 
les Gantt, les PV des réunions, les ordres du jour qui se trouvaient dans les mails. 

### Documents/Analyse

---
Les documents d'analyse sont ceux qui ont été présenté, à savoir :
* Le descriptif textuel du fonctionnement de l'application
* Les Use Case, qui permet de visualiser les fonctionnalités utilisateurs
* Les User Stories, qui représentent les fonctionnalités relatant le comportement de l'application

### Code

---
Ci-après se trouve la description de l'utilisation de l'application.

Concernant les fichiers, dans Code, il y a les dossiers "Communication" et "Tests" ainsi que le fichier `main.py`.
Ce dernier est le fichier à exécuter pour lancer l'application (cf. section suivante).

Dans "Code/Communication" se trouvent le code représentant les objets Python utilisés pour l'application : 
* Exception : ce fichier comporte la classe `NoDataError`, qui permet la gestion personnalisée de certaines erreurs.
* Connection : ce fichier comporte la classe `Connection`, qui permet la gestion du lancement de l'application.
* Certificate : ce fichier comporte la classe `Certificate`, qui permet la gestion des certificats pour les clients.
* Client : ce fichier comporte la classe `Client`, qui comporte toutes les méthodes utiles au bon fonctionnement d'un client comme (entre autres) :
  * Créer un réseau
  * Rejoindre un réseau
  * Répondre à des requêtes
  * Lister des fichiers
  * ... 

Dans "Code/Tests" se trouvent les fichiers permettant les tests de toutes les méthodes que nous avons écrites. 

## Utilisation de l'application

### Lancer l'application :

---
Pour lancer l'application, il faut d'abord se rendre dans le répertoire `Code` du projet et lancer les deux commandes suivantes :

````bash
pip install -r requirements.txt
python3 main.py
````



Vous allez d'abord installer les dépendances nécessaires au bon fonctionnement de l'application et ensuite la lancer.

Vous arriverez alors dans le menu suivant, où vous serez invité à sélectionner une option :

````bash
give the port you wanna use for socket connections (default is 8000) : 9000
the port 9000 will be use for socket connections

Press [1] to create a network.
Press [2] to join a network.
Press [q] to quit.
Choice: 
````
 
Vous devrez tout d'abord sélectionner le numéro de port sur lequel vous serez joignable. Si vous n'en fournissez pas, le port 8000 vous sera attribué par défaut.

Le premier choix permet de créer un réseau applicatif. Etant donné qu'aucun pair n'existe dans ce réseau, 
le terminal n'affichera rien car il attend que premier pair le contacte pour rejoindre l'application.
Ce qui représente la deuxième option. La dernière option permet de quitter l'application.

### Rejoindre le réseau

---
Lorsque la deuxième option est choisie, l'utilisateur doit entrer une adresse IP d'un pair présent sur le réseau ainsi que son port :

```bash
Press [1] to create a network. 
Press [2] to join a network.
Press [q] to quit.
Choice: 2

Enter peer to contact: 192.168.254.132
enter the port of the joined peer : 7000
```


Une fois l'adresse IP et le port entrés, voici ce qui est affiché à l'écran :

```bash
From peer: 'You are added to my peers list'

Actual peers list: ['192.168.254.1:9000', '192.168.254.132:7000']

Reaching out to all the peers...
Peers to contact : []
``` 

* Le pair qui vient de s'ajouter a reçu la confirmation comme quoi il a été ajouté à la liste des pairs du pair 
qu'il a contacté. 
* Le pair local a mis sa liste à jour avec l'aide de la liste reçue par le pair déjà présent avec 
d'abord son adresse IP à lui (192.168.254.1) et ensuite l'adresse IP du pair qu'il vient de contacter.
* Ensuite, le nouveau pair (192.168.254.1) va prendre contact avec tous les autres pairs de la liste afin que eux-même 
l'ajoutent à leur liste de pairs.
* Enfin, le menu de l'application s'affiche avec le choix de lister les fichiers 
disponibles, lister et télécharger un fichier ou bien quitter l'application. 


Tout en proposant ces actions, le pair reste disponible pour répondre à d'éventuelles requêtes.

## Menu principal

---
La première possibilité est de simplement lister les fichiers disponibles sur le réseau.
```bash
Select [1] to list files
Select [2] to list & download a file
Select [3] to join another network
Select [4] to show peers list
Hit 'q' to stop
Choice: 1

1. 01 - ScrumXP.pdf
2. test.txt
3. rapport-padr-2.pdf
4. final.txt
5. textrandom.txt
6. demo.mov
7. rapport-padr-2.docx
```


La seconde possibilité est de lister les fichiers disponibles sur le réseau et d'en choisir un à télécharger.

```bash
Enter the number of the file you want to download: 7
You chose the file: rapport-padr-2.docx
Sending certificate to 192.168.254.1
Receiving file
File received !
```

Les deux pairs s'échangent leurs certificats afin de mettre en place un canale de transfert sécurisé pour ce téléchargement de fichier.



La troisième option est celle permettant de fusionner 2 réseaux différents. Lorsque cette option est sélectionnée, il faut entrer
l'adresse IP et le numéro de port du pair : 

```bash
Enter peer to contact:
192.168.254.142
192.168.254.142 is a correct IP4 address.
Enter socket port of the peer to contact:
8000
```

Ensuite la fusion commence.

Enfin, la dernière option est de quitter l'application. Un message est envoyé à chaque pair pour qu'ils 
retirent le pair qui quitte le réseau de leur liste de pairs.

```bash
Select [1] to list files
Select [2] to list & download a file
Select [3] to join another network
Select [4] to show peers list
Choice: q
Peers to contact : ['192.168.254.132:7000']
```

