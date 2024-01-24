import os
import platform
import socket
import sys
import threading
import ipaddress


class Connection:
	def __init__(self, client):
		self.__client = client

	# getter
	@property
	def client(self):
		return self.__client

	@staticmethod
	def input_ip():
		try:
			ip_to_input = input("Enter peer to contact:\n")
			ip = ipaddress.ip_address(ip_to_input)
			if ip.version != 4:
				raise ValueError
			print('%s is a correct IP%s address.' % (ip, ip.version))
			return ip_to_input

		except ValueError:
			print("invalid IP, please enter a valid IPV4 address !")
			return Connection.input_ip()

	def manage_files(self, choice):
		"""
		Demande à l'utilisateur s'il souhaite lister ou sélectionner un fichier à télécharger ou bien
		s'il souhaite ne rien faire.
		:param choice: [string] Choix de l'utilisateur
		"""
		try:

			if choice == "1":
				self.client.list_files()
				return True

			elif choice == "2":
				owner_list = self.client.select_file_to_download()
				self.client.recv_file(owner_list)
				return True

			elif choice == "q":
				print("quit file options")
				return True

		except KeyboardInterrupt:
			print("ctrl-c exit")
			return False

	def initialize(self):
		initializing = input(
			"\nPress [1] to create a network.\nPress [2] to join a network.\nPress [q] to quit.\nChoice: ")

		while initializing != "1" and initializing != "2" and initializing != "q":
			print("\nPlease select [1], [2] or [q].\n")
			initializing = input(
				"\nPress [1] to create a network.\nPress [2] to join a network.\nPress [q] to quit.\nChoice: ")
		try:
			# Premier choix : Création d'un réseau
			# Ensuite, écoute et réponse aux nouvelles requêtes
			match initializing:
				# Premier choix : Création d'un réseau
				case "1":
					print("Waiting for 1st incoming connection")
					self.client.create_network()
					return True

				case "2":
					# Second choix : Rejoindre un réseau en contactant un pair.
					# Ensuite, le nouveau client prend contact avec les pairs présents dans la liste reçue.
					ip_to_contact = Connection.input_ip()
					self.client.join_network(ip_to_contact)
					self.client.reach_to_peers()
					return True

				case "q":
					os.remove(self.client.cert)
					os.remove(self.client.private_key)
					if platform.system() == "Windows":
						os.rmdir(".\\cert")
					elif platform.system() == "Linux" or platform.system() == "Darwin":
						os.rmdir("./cert")
					print("good bye !")
					return False

		except KeyboardInterrupt:
			print("ctrl-c exit")
			return False

		except socket.error:
			print("exception socket error")
			return False

	#TODO: à revoir
	def define_port(self):
		try:
			tmp_port = int(input("give the port you wanna use for socket connections (default is 8000) : "))
			print(f"the port {tmp_port} will be use for socket connections")
			self.client.port = tmp_port
		except:
			print("invalide port, 8000 will be use as socket port")

	def define_connection(self):
		self.define_port()
		connection_alive = self.initialize()

		# création du thread answer_request
		t1 = threading.Thread(target=self.client.answer_request, args=(), daemon=True)
		if connection_alive:
			t1.start()

		while connection_alive:
			try:
				print("\nSelect [1] to list files")
				print("Select [2] to list & download a file")
				print("Select [3] to join another network")
				print("Select [4] to show peers list")
				print("Hit 'q' to stop")
				choice = input("Choice: ")

				while choice != "1" and choice != "2" and choice != "3" and choice != "4" and choice != "q":
					print("\nPlease enter a correct option.")
					choice = input("Choice: ")

				if choice == "1" or choice == "2":
					# Ensuite, gestion de fichier et écoute et réponse aux nouvelles requêtes
					connection_alive = self.manage_files(choice)

				elif choice == "3":
					ip_to_merge = self.input_ip()
					port_to_input = int(input("Enter socket port of the peer to contact:\n"))
					last_peer_index = self.client.merge_request(ip_to_merge, port_to_input)
					self.client.send_merge(ip_to_merge, last_peer_index, port_to_input)

				elif choice == "4":
					print(self.client.peers)

				else:
					break

			except KeyboardInterrupt:
				connection_alive = False
				print("ctrl-c exit")

		# si l'utilisateur ferme avant d'avoir créé le thread, gestion de n'importe quelle exception

		self.client.disconnect()
		sys.exit()
