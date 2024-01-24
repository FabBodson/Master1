from Communication.Connection import Connection
from Communication.Client import Client


def main():
    # Création de l'objet Client
    client = Client()
    client.create_socket()
    # Création de l'objet Connection
    connection = Connection(client)
    # démarrage de la connection
    connection.define_connection()


if __name__ == "__main__":
    main()
