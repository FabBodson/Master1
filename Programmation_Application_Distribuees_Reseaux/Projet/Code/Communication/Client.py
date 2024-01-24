import socket
import pickle
import os
import platform
import random
import time
from Communication.Exception import NoDataError
from Communication.Certificate import Certificate, create_cert_repo
import ssl


def create_repo():
    rep = ""
    curr_platform = platform.system()
    if curr_platform == "Windows":
        rep = ".\\DistribAppShare"
    elif curr_platform == "Linux" or curr_platform == "Darwin":
        rep = "./DistribAppShare"

    try:
        if not os.path.exists(rep): #if not os.path.exists(f"./{rep}"):
            os.mkdir(rep)

    except os.error:
        print("Error while reading repository. Please check for permission error.")

    finally:
        return rep


class Client:
    # Initialisation d'un client
    def __init__(self):
        self.__repository = create_repo()
        # Create repository for SSL
        create_cert_repo()
        self.__ip = ""
        self.__peers = []
        self.__transfer_list = []
        self.__socket = None
        self.__repository_content = []
        self.files_dict = {}
        self.port = 8000
        if platform.system() == "Windows":
            self.__cert = ".\\cert\\my.crt"
            self.__private_key = ".\\cert\\private.key"
        elif platform.system() == "Linux" or platform.system() == "Darwin":
            self.__cert = "./cert/my.crt"
            self.__private_key = "./cert/private.key"

        # Génération clé privée + certificat peer
        Certificate(self.cert, self.private_key, "localhost")

    # getters and setters

    @property
    def cert(self):
        return self.__cert

    @property
    def private_key(self):
        return self.__private_key

    @property
    def repository(self):
        return self.__repository

    @property
    def ip(self):
        return self.__ip

    @ip.setter
    def ip(self, value):
        self.__ip = value

    @property
    def transfer_list(self):
        return self.__transfer_list

    @transfer_list.setter
    def transfer_list(self, value):
        self.__transfer_list = value

    @property
    def peers(self):
        """
        Le client aura toujours son adresse IP en premier dans la liste de pair ainsi que l'IP du premier
        pair qui a été contacté.
        """
        return self.__peers

    @peers.setter
    def peers(self, value):
        self.__peers = value

    @property
    def socket(self):
        return self.__socket

    @socket.setter
    def socket(self, value):
        self.__socket = value

    @cert.setter
    def cert(self, value):
        self.cert = value

    @private_key.setter
    def private_key(self, value):
        self.private_key = value

    @property
    def repository_content(self):
        return self.__repository_content

    @repository_content.setter
    def repository_content(self, value):
        self.__repository_content = value

    def recover_port(self, target_ip):
        for ip_port in self.peers:
            ip, port = ip_port.split(':')
            if ip == target_ip:
                return port
        return None

    def get_network_files(self):
        """
        Récupère les fichiers présents sur le réseau en allant contacter chaque pair de la liste.
        :return: La liste des fichiers, sans doublons, présents sur le réseau.
        """
        peers_to_contact = self.peers[1:]
        network_files = []

        for peer in peers_to_contact:
            self.create_socket()
            peer_ip = (peer.split(":"))[0]
            peer_port = (peer.split(":"))[1]
            self.socket.connect((peer_ip, int(peer_port)))

            msg = str.encode("Files request")
            self.socket.send(msg)

            peer_files = pickle.loads(self.socket.recv(2048))
            # alimente le dictionnaire avec {ip:nom_fichier, ...}
            self.files_dict[peer_ip] = peer_files
            for file in peer_files:
                if file not in network_files:
                    network_files.append(file)

            self.socket.close()
        return network_files

    def list_files(self):
        """
        Liste et affiche à l'écran les fichiers disponibles sur le réseau et en local.
        """
        try:
            if not os.path.exists(f"./{self.repository}"):
                os.mkdir(self.repository)

            self.repository_content = os.listdir(self.repository)

            network_files = self.get_network_files()
            for file in network_files:
                if file not in self.repository_content:
                    self.repository_content.append(file)

            if len(self.repository_content) == 0:
                print(f"The following repository has no element: {self.repository}")

            else:
                for element in range(len(self.repository_content)):
                    print(f"{element + 1}. {self.repository_content[element]}")

        except os.error:
            print("Error while reading repository. Please check for permission error.")

    def select_file_to_download(self):
        """
        Liste et affiche d'abord les fichiers disponibles. Ensuite, l'utilisateur doit sélectionner celui qu'il souhaite
        télécharger.
        """
        self.list_files()

        # Vérification que c'est bien un nombre
        correct_choice = False
        nbr = -1
        while correct_choice is False:
            nbr = input("Enter the number of the file you want to download: ")
            try:
                nbr = int(nbr)
                if 0 < nbr <= len(self.repository_content):
                    print(f"You chose the file: {self.repository_content[nbr - 1]}")
                    correct_choice = True
                else:
                    print("Please enter a valid number.")
            except ValueError:
                print("Value error, Please enter a valid number.")
        file_to_download = self.repository_content[nbr - 1]
        returned_list = [file_to_download]
        for ip, filesname in self.files_dict.items():
            for file in filesname:
                if file == file_to_download:
                    returned_list.append(ip)
        # on retourne une liste dont le premier élément est le nom du fichier et le reste est les pairs qui le possèdent
        return returned_list

    def create_socket(self):
        """
        Création du socket
        :return: Le socket créé
        """
        # Creation d'un objet socket : AF_INET pour communiquer en IPv4. SOCK_STREAM pour TCP.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Pour libérer le port après son utilisation
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def add_peer(self, peer_ip_port):
        """
        Ajoute un pair à la liste des pairs ou ne l'ajoute pas s'il s'y trouve déjà
        :param peer_ip: [str] Adresse IP du pair à ajouter
        :return: [(str), (list)] Tuple contenant d'abord le message à envoyer au pair et ensuite la liste des pairs à envoyer
        """
        if peer_ip_port not in self.peers:
            print(f"Added to peers.")

            msg = str.encode("You are added to my peers list")
            self.peers.append(peer_ip_port)
            list_of_peers = self.peers

            print(f"Actual peers list: {self.peers}\n")

        else:
            print("Peer is already in the peers list\n")

            msg = str.encode("You are already in the peers list")
            list_of_peers = self.peers

        return msg, list_of_peers

    def create_network(self):
        """
        Création d'un socket pour écouter les connexions qui demandent l'adhésion au réseau.
        Ensuite, ajout du nouveau client à la liste des pairs.
        Envoi de la liste de pairs.
        :param port: [int] Port de l'application, 8000
        :return: Fermeture de la connexion avec le client
        """
        self.socket.bind(('0.0.0.0', self.port))

        # Mise en attente d'une connexion
        self.socket.listen(0)

        # Récupération des informations, à savoir le socket pour la connexion avec le client
        # et les informations suivante sur le client : son adresse IP et le port utilisé
        connection, (peer_ip, peer_port) = self.socket.accept()

        conn_is_alive = True
        while conn_is_alive:
            try:
                # Réception des données, en bytes.
                data = connection.recv(2048)

                if not data:
                    raise NoDataError

                # Décodage et séparation de la string en liste pour une meilleure gestion du contenu
                data = (data.decode()).split(" ")
                print(f"From new peer: {data[0]} {data[1]}")

                # Le pair a envoyé l'IP qu'il souhaite joindre
                # L'ip est déterminée ainsi afin d'éviter d'avoir 127.0.0.1 en passsant par le hostname.
                self.ip = data[2]
                self.peers.append(f"{self.ip}:{self.port}")

                peer_port = data[6]
                # Récupération des informations et envoi au pair
                msg, list_of_peers = self.add_peer(f"{peer_ip}:{int(peer_port)}")
                connection.send(msg)
                time.sleep(0.2)
                connection.send(pickle.dumps(list_of_peers))

            except NoDataError:
                conn_is_alive = False

            except socket.error:
                print("exception socket error")
                conn_is_alive = False

        connection.close()

    def join_network(self, ip_to_reach):
        """
        Permet de rejoindre un réseau en contactant l'adresse IP fournie
        :param ip_to_reach: Adresse IP entrée à contacter pour rejoindre le réseau de pairs
        :param port: port de l'application, 8000
        :return: Connexion fermée
        """
        tmp_port = int(input("enter the port of the joined peer : "))
        self.socket.connect((ip_to_reach, tmp_port))

        msg = str.encode(f"Join request {ip_to_reach} i listen on {self.port}")
        self.socket.send(msg)

        # Réception de la liste des pairs et de l'adresse IP du client.
        # L'ip est déterminée ainsi afin d'éviter d'avoir 127.0.0.1 en passsant par le hostname.
        data = self.socket.recv(2048)
        data = data.decode()
        self.peers = pickle.loads(self.socket.recv(2048))

        if data.split(" ")[2] == "added":
            ip_port = (self.peers[-1])
            self.ip = (ip_port.split(":"))[0]  # récupérer juste l'ip de la dernière entrée de la liste
            # Pour garder l'IP du client en première dans la liste de pairs, celle-ci est retirée puis ajoutée
            # au début de la liste.
            self.peers.pop()
            self.peers.insert(0, ip_port)

        print(f"\nFrom peer: '{data}'\n")
        print(f"Actual peers list: {self.peers}\n")

        self.socket.close()

    def answer_request(self):
        """
        Actions prises en fonction d'une requête reçue
        :param port: [int] Port utilisé par l'application
        :return: Les actions prises et fermeture de la connexion
        """

        conn_is_alive = True
        while conn_is_alive:
            try:

                self.create_socket()
                self.socket.bind(('0.0.0.0', self.port))
                # Mise en attente d'une connexion
                self.socket.listen(0)

                # Récupération des informations, à savoir le socket pour la connexion avec le client
                # et les informations suivante sur le client : son adresse IP et le port utilisé
                connection, (peer_ip, peer_rand_port) = self.socket.accept()

                # Réception des données, en bytes
                data = connection.recv(2048)
                try:
                    pickle.loads(data)
                except:
                    # Décodage et séparation de la string en liste pour une meilleure gestion du contenu
                    data = (data.decode()).split(" ")

                if not data:
                    raise NoDataError

                # Réception d'une demande pour rejoindre le réseau ou une demande de contact
                if data[0] == "Join":
                    print(f"From new peer: {data[0]} {data[1]}")

                    msg, list_of_peers = self.add_peer(f"{peer_ip}:{data[6]}")
                    connection.send(msg)
                    time.sleep(0.5)
                    connection.send(pickle.dumps(list_of_peers))

                elif data[0] == "Contact":
                    print(f"From new peer: {data[0]} {data[1]}")

                    msg, list_of_peers = self.add_peer(f"{peer_ip}:{data[6]}")
                    connection.send(msg)


                elif data[0] == "Files":
                    print(f"\nPeer requested shared files.")
                    self.repository_content = os.listdir(self.repository)
                    connection.send(pickle.dumps(self.repository_content))

                elif data[0] == "Ask":
                    file = data[1]
                    self.send_file(peer_ip, file, connection)

                elif data[0] == "Merge":
                    print("Merge request received")
                    connection.send(pickle.dumps(self.peers))

                elif data[0] == "New":
                    print("Merging to a new network")
                    new_peers = pickle.loads(connection.recv(2048))
                    for new_peer in new_peers:
                        self.add_peer(new_peer)
                    self.reach_to_peers()

                elif data[0] == "in_transfer":
                    if data[1] not in self.transfer_list:
                        self.transfer_list.append(data[1])

                elif data[0] == "not_in_transfer":
                    if data[1] in self.transfer_list:
                        self.transfer_list.remove(data[1])

                elif data[0] == "Disconnect":
                    print(f"{peer_ip} is disconnected !")
                    for peer in self.peers:
                        if (peer.split(":"))[0] == peer_ip:
                            self.peers.remove(peer)

                elif data[0] == "s-cert":
                    print(f"Sending certificate to {peer_ip}")
                    self.send_cert(peer_ip)
                    self.ask_for_cert(peer_ip, int(self.recover_port(peer_ip)), 'receive')
                    print(f"Receiving certificate from {peer_ip}")
                    self.recv_cert(peer_ip)

                elif data[0] == "r-cert":
                    print(f"Sending certificate to {peer_ip}")
                    self.send_cert(peer_ip)
                else:
                    continue
                connection.close()

            except NoDataError:
                print("No data, connexion isn't alive anymore.\n")
                conn_is_alive = False

            except socket.error:
                print("exception socket error")
                conn_is_alive = False

            except os.error:
                print("3 Error while reading repository. Please check for permission error.")
                conn_is_alive = False

    def reach_to_peers(self):
        """
        Prise de contact avec les pairs de la liste de pairs
        :param port: [int] Port utilisé par l'application
        :return: Fermeture de la connexion et la liste de pairs à jour
        """

        print("Reaching out to all the peers...")

        # Liste reprenant les pairs à contacter, hors les 2 premières qui correspondent
        # à l'IP de l'hôte et du pair contacté pour rejoindre le réseau
        peers_to_contact = self.peers[2:]

        print(f"Peers to contact : {peers_to_contact}\n")

        for peer in peers_to_contact:
            peer_ip = (peer.split(":"))[0]
            peer_port = (peer.split(":"))[1]
            self.create_socket()
            self.socket.connect((peer_ip, int(peer_port)))

            # Envoi de mon IP et de la demande de contact
            msg = str.encode(f"Contact request {self.ip} I listen on {self.port}")
            self.socket.send(msg)
            #time.sleep(0.5)

            # Réception des données, en bytes
            data = self.socket.recv(2048)
            #time.sleep(0.5)

            print(f"\nFrom peer: '{data.decode()}'\n")

            self.socket.close()

    def disconnect(self):
        """
        Prise de contact avec les pairs de la liste de pairs pour qu'ils suppriment le pair local de leur liste
        :param port: [int] Port utilisé par l'application
        :return: Fermeture de la connexion et la liste de pairs à jour
        """

        # Liste reprenant les pairs à contacter, hors la première qui correspond
        # à l'IP de l'hôte
        peers_to_contact = self.peers[1:]

        print(f"Peers to contact : {peers_to_contact}\n")

        for peer in peers_to_contact:
            peer_ip = (peer.split(":"))[0]
            peer_port = (peer.split(":"))[1]
            self.create_socket()
            self.socket.connect((peer_ip, int(peer_port)))

            # Envoi de la notification de la deconnexion
            msg = str.encode("Disconnect")
            self.socket.send(msg)

            self.socket.close()

    def in_transfer(self, state, ip):
        """
        Cette fonction permet de définir l'état d'un pair comme étant occupé par un transfert de fichier.
        :param state: [string] En transfert ou non ("in_transfer" ou "not_in_transfer")
        :param ip: [string] Adresse IP de la machine concernée
        :param port: [int] Port utilisé
        :return: L'état de la machine
        """
        # state -> not_in_transfer or in_transfer
        array = [state, ip]
        if state == "in_transfer":
            if ip not in self.transfer_list:
                self.transfer_list.append(ip)

        elif state == "not_in_transfer":
            if ip in self.transfer_list:
                self.transfer_list.remove(ip)

        for peer in self.peers[1::]:
            peer_ip = (peer.split(":"))[0]
            peer_port = (peer.split(":"))[1]
            self.create_socket()
            self.socket.connect((peer_ip, int(peer_port)))
            self.socket.send(pickle.dumps(array))

    def send_file(self, peer, filename, client_socket):
        self.in_transfer("in_transfer", peer)
        time.sleep(0.5)

        if platform.system() == "Windows":
            path = f".\\DistribAppShare\\{filename}"
        else:
            path = f"./DistribAppShare/{filename}"

        # Configurer le contexte SSL/TLS
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile=self.cert, keyfile=self.private_key)

        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Boucle principale pour accepter les connexions des clients
        try:
            # Configurer le socket SSL/TLS
            ssl_socket = context.wrap_socket(client_socket, server_side=True)

            print("Sending file...")
            with open(path, "rb") as f:
                fb = f.read(2048)
                while len(fb) != 0:
                    ssl_socket.sendall(fb)
                    fb = f.read(2048)
                print("File sended !")

        except Exception as e:
            print("Erreur lors de l'acceptation d'une connexion client :", e)

        time.sleep(0.5)
        self.in_transfer("not_in_transfer", peer)
        client_socket.close()

    def recv_file(self, owner_list):
        selected_peer = None
        filename = owner_list[0]
        for peer in owner_list[1:]:
            if peer in self.transfer_list:
                pass
            elif peer not in self.transfer_list:
                selected_peer = peer
        if selected_peer == None:
            selected_peer = random.choice(owner_list[1:])


        # Cert exchange
        self.ask_for_cert(selected_peer, int(self.recover_port(selected_peer)), 'send')
        self.recv_cert(selected_peer)

        # Waiting to cert process to finish
        time.sleep(5)

        message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message_socket.connect((selected_peer, int(self.recover_port(selected_peer))))
        msg = str.encode(f"Ask {filename}")
        message_socket.send(msg)

        time.sleep(1)

        # connection, (peer_ip, peer_port) = transaction_socket.accept()
        if platform.system() == "Windows":
            path = f".\\DistribAppShare\\{filename}"
        else:
            path = f"./DistribAppShare/{filename}"

        # Configurer le contexte SSL/TLS
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Charger le certificat auto-signé pour la vérification
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE

        # Connexion au serveur en utilisant SSL/TLS
        with context.wrap_socket(message_socket, server_hostname=selected_peer) as ssl_socket:
            print("Receiving file")
            with open(path, "wb") as f:
                fb = ssl_socket.recv(2048)
                while len(fb) != 0:
                    f.write(fb)
                    fb = ssl_socket.recv(2048)

            print("File received !")

        message_socket.close()

    def merge_request(self, ip_to_merge, port_to_merge):
        """
        Cette méthode permet de débuter un merge en contactant une adresse IP d'un autre réseau.
        :param ip_to_merge: [string] Adresse IP à contacter
        :param port: [int] Port utilisé
        :return: [int] La taille de la liste de pair originale
        """
        if ip_to_merge not in self.peers:
            self.create_socket()
            self.socket.connect((ip_to_merge, port_to_merge))

            msg = str.encode(f"Merge request {ip_to_merge}")
            self.socket.send(msg)
            #time.sleep(1)

            # Réception de la liste des pairs du nouveau réseau.
            new_peers = pickle.loads(self.socket.recv(2048))
            # La taille de la liste de pair originale est récupérer avant modification
            # afin de l'utiliser comme index pour contacter les anciens pairs (voir méthode send_merge)
            last_peer_index = len(self.peers)

            for new_peer in new_peers:
                if new_peer not in self.peers:
                    self.peers.append(new_peer)

            self.reach_to_peers()
            self.socket.close()
            print(f"New peers list: {self.peers}\n")
            return last_peer_index

    def send_merge(self, ip_to_merge, last_peer_index, port_to_merge):
        """
        Cette méthode permet de contacter chaque pair du réseau originel afin de leur faire savoir qu'il y a un merge
        à faire.
        :param ip_to_merge: [string] Adresse IP à contacter pour fusionner
        :param last_peer_index: [int] Index pointant l'emplacement de la denrière IP de la liste de paire originelle
        :param port: [int] Port utilisé
        :return: True pour maintenir la connexion en vie (voir méthode define_connection)
        """
        print("Sending merge info to peers")
        for peer in self.peers[1:last_peer_index]:
            peer_ip = (peer.split(":"))[0]
            peer_port = (peer.split(":"))[1]
            self.create_socket()
            self.socket.connect((peer_ip, int(peer_port)))

            msg = str.encode(f"New network with {ip_to_merge}")
            self.socket.send(msg)

            time.sleep(1)
            self.socket.send(pickle.dumps(self.peers))

            self.socket.close()

        return True

    def send_cert(self, peer_ip, peer_cert_port=10000):
        """
        Cette fonction permet d'envoyer son certificat à un pair qui le demande.
        :peer_ip: [string] IP de la paire à qui on demande le certificat.
        :peer_cert_port: [int] Port utilisé. Par défaut le 10.000.
        :return: Le certificat envoyé
        """
        transaction_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transaction_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transaction_socket.connect((peer_ip, peer_cert_port))

        with open(self.cert, "rb") as f:
            fb = f.read(2048)
            while len(fb) != 0:
                transaction_socket.sendall(fb)
                fb = f.read(2048)

        transaction_socket.close()

    def recv_cert(self, peer_ip, peer_cert_port=10000):
        """
        Cette fonction permet de recevoir un certificat de la part d'un pair qui nous l'envoie.
        :peer_ip: [string] IP de la paire à qui on demande le certificat.
        :peer_cert_port: [int] Port utilisé. Par défaut le 10.000.
        :return: Le certificat est reçu.
        """
        transaction_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transaction_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        transaction_socket.bind((self.ip, peer_cert_port))
        transaction_socket.listen(0)

        connection, (peer_ip, peer_cert_port) = transaction_socket.accept()
        if platform.system() == "Windows":
            path = f".\\cert\\{peer_ip}.crt"
        else:
            path = f"./cert/{peer_ip}.crt"
        with open(path, "wb") as f:
            fb = connection.recv(2048)
            while len(fb) != 0:
                f.write(fb)
                fb = connection.recv(2048)

        connection.close()

    def ask_for_cert(self, peer_ip, peer_port, text):
        """
        Cette fonction permet de demander à cun pair d'envoyer son certificat où à sa préparer à en recevoir un
        en lui envoyant un message.
        :peer_ip: [string] IP de la paire à qui on demande le certificat.
        :peer_port: [int] Port utilisé par le pair afin de le contacter.
        :text: [string] String précisant à envoyer ou à recevoir un certificat.
        :return: Le message est envoyé.
        """
        message_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        message_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        message_socket.connect((peer_ip, peer_port))
        if text == "send":
            msg = str.encode(f"s-cert")
        else:
            msg = str.encode(f"r-cert")
        message_socket.send(msg)

        message_socket.close()
