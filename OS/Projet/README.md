# Systèmes d'exploitation : projet


## Organisation du repo Git

---
À la racine de ce projet, vous trouverez quatre répertoires : 
* **Ansible** : Ce répertoire contient tous les fichiers de configuration utilisés pour le déploiement Ansible.
* **Ressources** : Ici se trouve les différentes ressources que j'ai pu consulter pour réaliser les tâches du projet.
C'est pourquoi je ne détaillerai pas les configurations de chaque service dans ce README, j'y détaille uniquement ce qui semble
intéressant à noter. Je vous invite à consulter ces ressources pour connaitre les détails.
* **certs** : Ici se trouvent toutes les informations concernant le certificat Let's Encrypt utilisé pour assurer la 
sécurité des communications avec les services.
* **apps** : Celui-ci contient des sous-répertoires qui correspondent à chaque service. Et dans ces sous-répertoires, 
se trouvent les docker-compose qui correspondent à la configuration pour chaque service.

## Informations pratiques sur les VMs

---
Les VMs utilisées sont : 
- Fedora 36 en tant que serveur LDAP et DNS : `192.168.254.29`
- Debian 11 en tant que serveur hébergeant les services tournant avec Docker : `192.168.254.34`
- Fedora 36 utilisée pour Ansible : `192.168.254.42`
- Debian 11 utilisée pour Ansible : `192.168.254.39`
- Ubuntu 22 comme controleur Ansible : ``192.168.254.26``
- Le client UBuntu 22 : ``192.168.254.35``
- Le client Windows 10 : ``192.168.254.36``

Afin de simplifier la réalisation du projet, et donc dans le cadre du cours, j'ai opté pour le même nom d'utilisateur 
(`fabrice`) et le même mot de passe (`rootroot`) sur chaque VM. Il est bien entendu que dans le monde réel il faut
utiliser un mot de passe différent et complexe.

## LDAP

---
Le service d'annuaire open-source SAMBA a été utilisé. Le nom de domaine choisi est ``supercompta.com``.

Les noms de domaine utilisés par les conteneurs sont les suivants :
- `traefik.supercompta.com`
- `gitlab.supercompta.com`
- `nextcloud.supercompta.com`
- `meet.supercompta.com`
- `manage.supercompta.com`

La VM Fedora36 qui héberge le service LDAP sert de serveur DNS aux machines du domaine, elle pointe donc ces noms vers
l'adresse IP hébergeant les conteneurs, à savoir la debian 11.

Afin de créer les utilisateurs ainsi que les groupes associés et leur donner des noms, un script Python a été ecrit.


## Les services : Conteneurs

---
### Reverse proxy : traefik

La solution de reverse proxy choisie est celle de *traefik* car il existe beaucoup de documentation en plus de l'officielle 
qui est très complète. Cette solution est facile à utiliser avec Docker et est légère. 

**Configuration :**

1) La première étape a été de créer un réseau Docker dans lequel se trouveront tous les conteneurs qui seront 
impacté par le reverse proxy.


2) Ensuite, le docker-compose.yml a été écrit afin d'y retrouver les configurations requises.
   * La dernière version de l'image est utilisée
   * Le conteneur doit redémarrer à chaque fois s'il rencontre un bug
   * Il va rediriger les ports 80 et 443 vers les mêmes ports en interne
   * Il va utiliser des volumes afin de conserver toutes les informations en dehors du conteneur afin de pouvoir les 
   réutiliser facilement.
   * Il utilise le réseau Docker créé
   * Enfin, il faut lui préciser les options, nommées ``labels``, qui sont utilisées par le reverse proxy.


3) La 3ème étape a été de créer 2 autres fichiers afin d'y placer d'autres configurations modulables :
   * Les ``entrypoints`` et la `redirections` qui permettent de définir les ports d'entrée et le port de sortie
   * Le certificat à utiliser ainsi que des informations autour de celui-ci.



### GitLab
**Configuration :**

1) Le docker-compose contient les informations utiles au lancement de GitLab :
   * La dernière version de l'image de GitLab est utilisée.
   * Le conteneur doit toujours redémarrer en cas de soucis rencontré.
   * Je définis le nom de l'hôte sur `gitlab.supercompta.com` afin de lier le conteneur au nom de domaine
   * Les options pour traefik.
   * Les volumes à utiliser pour éviter de stocker les données importantes sur un conteneur.
   * L'utilisation du réseau Docker créé.


2) Lien avec le LDAP :
   * Il a fallu ajouter un utilisateur gitlab dans l'annuaire LDAP
   * Ensuite, dans un fichier de configuration présent dans les volumes, les informations pour utiliser
   le LDAP ont été ajoutées.

### Nextcloud
**Configuration :**

1) Le docker-compose contient les informations utiles au lancement de NextCloud :
   * Les 3 services utilisés pour faire tourner Nextcloud : 
     * Une base de données MariaDB
     * Un registry pour la mémoire cache Redis
     * L'application Nextcloud
   * Nextcloud dépend des 2 premiers services, il ne pourra donc pas se lancer si l'un de ces 2 là
   n'a pas démarré correctement.
   * Je définis le nom de l'hôte sur `nextcloud.supercompta.com` afin de lier le conteneur au nom de domaine
   * Le conteneur utilise 2 réseaux Docker : celui créé et celui par défaut. L'utilisation de celui par défaut
   se fait car les 2 premiers services tournent dans ce réseau par défaut.
   * Les options pour traefik.


2) Lien avec le LDAP :
   * Il faut se rendre dans le conteneur au moyen de la commande : `docker exec -it -u www-data nextcloud bash`
   * Et modifier la configuration afin d'utiliser le LDAP configuré.


### Jitsi Meet
Etant donné que le projet Jitsi est libre d'accès sur GitHub, il a suffi de le télécharger et de l'adapter à mon 
architecture.
L'application Jitsi est composée de 4 conteneurs de base pour son fonctionnement :

* Jitsi Meet (`web`) - Application web.
* Prosody (`prosody`) - Serveur XMPP.
* Jitsi Videobridge (`jvb`) - Permet d'acheminer les flux vidéo entre les participants d'une conférence.
* Jitsi Conference Focus (`jicofo`) - Permet la mise au point dans les conférences Jitsi Meet.

Il est possible d'ajouter encore 2 autres services permettant l'enregistrement et le streaming (`jibri`) et à d'autres 
membres de rejoindre la réunion (`jigasi`).

**Configuration :**
   * Ajouter l'utilisation du réseau docker traefik ainsi que les options requises dans chaque conteneur.
   * Utilisation d'un réseau jitsi pour réunir les services Jitsi dans le même réseau.
   * Écriture dans un fichier .env :
     * LDAP
     * URL publique (`meet.supercompta.com`)
     * Ports utilisés (80, 443)

### Serveur web Java pour la gestion du LDAP
**Configuration :**
   * Docker compose : 
     * Il utilise le Dockerfile écrit et le build.
     * Il utilise aussi les options pour passer par traefik
     * Nom de domaine : `manage.supercompta.com`
   * Dockerfile :
     * Utilisation du multistage build
     * J'ajoute d'abord les ressources nécessaires au build et à la compilation (pom.xml et les src/)
     * Je build en utilisant maven
     * Je compile le résultat obtenu une fois la première étape terminée
     * Compilation du fichier .jar produit
   * Code source utilisant l'outil Spring Boot :
     * Les pages HTML se trouvent dans src/main/resources/templates
     * Le code Java se trouve dans src/main/java/com/supercompta/manageldap :
       * Le main pour l'exécution de l'app dans ManageLdapApplication.java
       * Une classe utilisateur dans model/User.java
       * La classe permettant la gestion du LDAP dans la classe controller/ManageLdap.java

La classe ManageLdap possède plusieurs méthodes :
   - Connect afin d'établir une connexion vers le LDAP
   - searchUsers afin de rechercher un utilisateur
   - addUser afin d'ajouter un utilisateur
   - deleteUser afin de supprimer un utilisateur
   - authUser afin d'authentifier l'utilisateur qui se connecte (pour vérifier qu'il fait bien partie des techniciens)

*Pour information* :
> L'accès à la page d'authentification et l'authentification fonctionnent. Je suis bien redirigé vers la page suivante 
> (où je dois sélectionner l'aciton à prendre) mais je n'obtiens aucun utilisateur. Si je décide d'en ajouter un alors
> j'ai une erreur.


## Ansible

---

Pour la bonne réalisation de cette partie, 2 nouvelles VM Fedora et Debian ont été créées et des snapshots des 
configurations de base ont été faites afin de mener les tests le plus facilement possible.

Cette partie a été divisée en 2 parties : la mise en place de l'AD et la mise en place de DOcker et de ses services.
C'est pourquoi vous retrouverez 2 playbooks, chacun correspond à la partie :
- ``plbk-ad.yml`` pour l'AD
- ``plbk-install-docker.yml`` pour Docker

Aussi, un fichier `hosts` reprenant les informations nécessaires pour contacter les hôtes concernées facilement a été créé.
Dernièrement, un fichier `ansible.cfg` a été créé afin de reprendre des configurations générales.


### A) Playbook 1 : Mise en place de l'AD
#### a) Le playbook
Le playbook nommé ``plbk-ad.yml`` assure le déploiement de l'AD sur une machine Fedora au moyen du rôle `deploy` et 
du tag du même nom.

Il suffit alors d'utiliser la commande `ansible-playbook -K plbk-ad.yml --tags deploy` pour lancer le déploiement. Le -K
permet d'entrer le mot de passe pour devenir utilisateur root sur la machine distante. Cela est possible grâce à
l'instruction ``become: true`` du playbook.

#### b) Le rôle
Le rôle est divisé en 5 répertoires :
1) **defaults** : on y retrouve les variables utilisées par les tâches.
2) **files** : on y retrouve les fichiers utilisés par les tâches, ceux qu'il faut copier sur le conteneur.
3) **handlers** : on y retrouve les actions enclenchées à la fin de l'exécution du script lorsque les triggers 
de mêmes noms sont appelés.
4) **meta** : ceci contient une fiche descriptive de l'auteur du projet et quelques informations.
5) **tasks** : ici se trouvent les tâches nécessaires pour le déploiement de l'AD

*Pour information* :

L'ajout des entrées DNS rencontre une erreur pour l'ajout, que ce soit via Ansible ou même sur la première Fedora : 

> Failed to bind to uuid 50abc2a4-574d-40b3-9d66-ee4fd5fba076 for ncacn_ip_tcp:192.168.254.29[49152,sign,abstract_syntax=50abc2a4-574d-40b3-9d66-ee4fd5fba076/0x00000005,localaddress=192.168.254.29] NT_STATUS_RPC_UNSUPPORTED_NAME_SYNTAX
ERROR: Connecting to DNS RPC server 192.168.254.29 failed with (3221356582, 'The name syntax is not supported.')

### B) Playbook 2 : Mise en place de Docker et de ses services
#### a) Le playbook
Le playbook nommé ``plbk-install-docker.yml`` assure le déploiement de Docker et des services requis sur une machine 
Debian au moyen des rôles `install_docker` et `install_services` et des tags du même nom.

Il suffit alors d'utiliser la commande `ansible-playbook -K plbk-install-docker.yml` avec l'ajout d'un des tags si 
on veut cibler l'un des deux déploiements pour lancer le déploiement. Le -K permet d'entrer le mot de passe pour 
devenir utilisateur root sur la machine distante. Cela est possible grâce à l'instruction ``become: true`` du playbook.

#### b) Le rôle *install_docker*
Le rôle est divisé en 1 répertoire :
1) **tasks** : ici se trouvent les tâches nécessaires pour le déploiement des différents packages utiles à Docker

#### c) Le rôle *install_services*
Le rôle est divisé en 2 répertoires :
1) **tasks** : ici se trouvent les tâches nécessaires pour le déploiement des différents services
2) **files** : on y retrouve les fichiers utilisés par les tâches, ceux qu'il faut copier sur le conteneur.

*Pour information* :
> Tous les conteneurs se trouvent dans le même docker-compose contrairement à avant.
