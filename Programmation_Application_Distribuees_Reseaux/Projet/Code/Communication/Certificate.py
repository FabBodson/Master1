from OpenSSL import crypto
import platform
import os


def create_cert_repo():
    """
    Crée le répertoire cert pour contenir les certificats ainsi que la clé privée.
    :return: Le répertoire créé
    """
    rep = ""
    curr_platform = platform.system()
    if curr_platform == "Windows":
        rep = ".\\cert"
    elif curr_platform == "Linux" or curr_platform == "Darwin":
        rep = "./cert"

    try:
        if not os.path.exists(rep):
            os.mkdir(rep)
        else:
            cleanup_mess(rep)
            os.mkdir(rep)

    except os.error:
        print("Error while reading repository. Please check for permission error.")


def cleanup_mess(mess):
    """
    Cette fonction supprime le répertoire cert ainsi que les fichiers qui ont été créés dedans.
    :param mess: Chemin vers le répertoire cert/
    :return: Le répertoire cert est supprimé
    """
    if os.path.exists(mess):
        for filename in os.listdir(mess):
            path = os.path.join(mess, filename)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                cleanup_mess(path)
        os.rmdir(mess)


class Certificate:
    """
    Cette classe représente l'objet Certificat afin qu'il contienne tous les champs nécessaires dans un certificat.
    """
    def __init__(self, cert_file, key_file, subject):
        # Création d'une clé privée de 2048 bits
        self.__private_key = crypto.PKey()
        self.private_key.generate_key(crypto.TYPE_RSA, 2048)

        # Création d'un certificat auto-signé
        self.__cert = crypto.X509()
        self.cert.get_subject().CN = subject
        self.cert.get_subject().O = "My Organization"
        self.cert.get_subject().OU = "My Organizational Unit"
        self.cert.set_serial_number(1000)
        self.cert.gmtime_adj_notBefore(0)
        self.cert.gmtime_adj_notAfter(24 * 60 * 60)  # Durée de vie d'un jour
        self.cert.set_issuer(self.cert.get_subject())
        self.cert.set_pubkey(self.private_key)
        self.cert.sign(self.private_key, "sha256")

        with open(cert_file, "wt") as f:
            f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, self.cert).decode("utf-8"))

        with open(key_file, "wt") as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.private_key).decode("utf-8"))

    @property
    def cert(self):
        return self.__cert

    @property
    def private_key(self):
        return self.__private_key

    @cert.setter
    def cert(self, value):
        self.cert = value

    @private_key.setter
    def private_key(self, value):
        self.private_key = value
