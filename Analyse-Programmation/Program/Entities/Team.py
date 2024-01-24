from Program.Entities.Warrior import Warrior
from Program.Entities.Thief import Thief
from Program.Entities.Magus import Magus
from Program.Entities.Healer import Healer
from random import choice
import sqlite3


class Team:
    def __init__(self, name):
        self.__name = name
        self.__members = []
        self.__size = 0
        self.__tactic = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def members(self):
        return self.__members

    @members.setter
    def members(self, value):
        self.__members = value

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, value):
        self.__size = value

    @property
    def tactic(self):
        return self.__tactic

    @tactic.setter
    def tactic(self, value):
        self.__tactic = value

    def select_members(self):
        """
        Sélection de 10 joueurs à ajouter dans l'équipe
        """
        db = sqlite3.connect('game.db')
        cursor = db.cursor()

        for _ in range(10):
            cursor.execute("SELECT * FROM Players WHERE is_selected = 0 AND is_alive = 1 ORDER BY RANDOM() LIMIT 1")
            user = cursor.fetchone()

            if user[2] == "Warrior":
                # id, name, category, attack, defense, life, critical_hit, initiative, parade
                member = Warrior(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7],
                                 user[11])
                self.members.append(member)

            elif user[2] == "Thief":
                # id, name, category, attack, defense, life, critical_hit, initiative, dodge
                member = Thief(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7],
                               user[10])
                self.members.append(member)

            elif user[2] == "Magus":
                # id, name, category, attack, defense, life, critical_hit, initiative
                member = Magus(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7])
                self.members.append(member)

            elif user[2] == "Healer":
                # id, name, category, attack, defense, life, critical_hit, initiative, parade, heal
                member = Healer(user[0], user[1], user[2], user[3], user[4], user[5], user[6], user[7],
                                user[11], user[12])
                self.members.append(member)

            update = "UPDATE Players SET is_selected = 1 WHERE Player_ID = ?"
            cursor.execute(update, (user[0],))
            db.commit()

        # Mise à jour de la taille de l'équipe
        self.size = len(self.members)

        db.close()

    def remove_member(self, member):
        """
        Suppression d'un membre de l'équipe
        : param member : [Objet Entité] Membre de l'équipe
        """
        db = sqlite3.connect('game.db')
        cursor = db.cursor()

        update = "UPDATE Players SET is_selected = 0 WHERE Player_ID = ?"
        cursor.execute(update, (member.id,))
        db.commit()

        self.members.remove(member)

        # Mise à jour de la taille de l'équipe
        self.size = len(self.members)

        db.close()

    def select_tactic(self):
        """
        Sélection d'une tactique
        """
        db = sqlite3.connect('game.db')
        cursor = db.cursor()

        cursor.execute("SELECT * FROM Tactics ORDER BY RANDOM() LIMIT 1")

        # Récupération de l'ID de la tactique utilisée
        self.tactic = cursor.fetchone()

        db.commit()
        db.close()

    def print_info(self):
        """
        Affiche des informations sur l'équipe
        """
        print(f"\nTeam {self.name} information :")
        # Affichage du nom de la tactique utilisée
        print(f"Tactic: {self.tactic[1]}")
        print("Members:")
        for member in self.members:
            print(f"{member.name} the {member.category}. Life : {member.life}")
