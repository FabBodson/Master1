from random import randint
import sqlite3


class Entity:
    # Chaque entité posssède ces caractéristiques-ci
    def __init__(self, id, name, category, attack, defense, life, critical_hit, initiative):
        self.__id = id
        self.__name = name
        self.__category = category
        self.__attack = attack
        self.__defense = defense
        self.__life = life
        self.__critical_hit = critical_hit
        self.__initiative = initiative
        self.original_life = life
        self.__is_fighting = False

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def category(self):
        return self.__category

    @property
    def attack(self):
        return self.__attack

    @property
    def defense(self):
        return self.__defense

    @property
    def life(self):
        return self.__life

    @life.setter
    def life(self, value):
        self.__life = value

    @property
    def critical_hit(self):
        return self.__critical_hit

    @property
    def initiative(self):
        return self.__initiative

    @property
    def is_fighting(self):
        return self.__is_fighting

    @is_fighting.setter
    def is_fighting(self, value):
        self.__is_fighting = value

    def take_hit(self, damage):
        """
        Retire des points de vies et met la vie à 0 si celle-ci devient négative
        :param damage : [int] Les points de vie à retirer
        : return : La vie mise à jour
        """
        db = sqlite3.connect('game.db')
        cursor = db.cursor()

        self.__life = self.__life - damage
        if self.__life < 0:
            self.__life = 0

        update = "UPDATE Players SET life = ? WHERE Player_ID = ?"
        cursor.execute(update, (self.life, self.id))
        db.commit()
        db.close()

        return self.__life

    def is_alive(self):
        """
        Vérifie si le joueur est en vie ou non
        : return : Booleen
        """
        if self.life > 0:
            return True
        else:
            db = sqlite3.connect('game.db')
            cursor = db.cursor()

            update = "UPDATE Players SET is_alive = 0 WHERE Player_ID = ?"
            cursor.execute(update, (self.id,))

            # Suppression de la dernière occurrence du joueur dans la table afin de ne pas supprimer son apparition dans
            # d'anciennes parties
            delete = "DELETE FROM Players_alive WHERE Player_ID = ? ORDER BY Game_ID DESC LIMIT 1"
            cursor.execute(delete, (self.id,))

            db.commit()
            db.close()
            return False

    def attack_can_go_on(self, victim):
        """
        Vérifie si la victime esquive ou pare l'attaque.
        :param victim: [Objet Entité] Victime attaquée
        :return: Booleen
        """
        if (victim.category in ("Warrior", "Healer")) and (randint(1, 100) <= victim.parade):
            print(f"{victim.name} the {victim.category} has parried the attack of {self.name} the {self.category}")
            return False

        elif (victim.category is "Thief") and (randint(1, 100) <= victim.dodge):
            print(f"{victim.name} the {victim.category} has dodged the attack of {self.name} the {self.category}")
            return False

        return True

    def attack_victim(self, victim, damages, critical):
        """
        Attaque la victime, affiche un message si c'était avec ou sans coup critique.
        :param victim: [Objet Entité] Victime attaquée
        :param damages : [int] Degats à infliger
        :param critical : [bool] Attaque critique ou non
        : return : Affiche des messages
        """
        previous_life = victim.life
        victim.take_hit(damages)
        if critical is True:
            print(f"{self.name} the {self.category} attacked critically {victim.name} the {victim.category} !")
            print(f"Critical attack of {damages} !")
        else:
            print(f"{self.name} the {self.category} attacked {victim.name} the {victim.category} !")
            print(f"Attack of {damages} !")

        print(f"Victim's life went from {previous_life} to {victim.life}")

    def use_attack_on(self, victim, critical):
        """
        Utilise l'attaque sur une victime, les dégats varient selon si c'est un coup critique ou non.
        :param victim: [Objet Entité] Victime attaquée
        :param critical: [bool] Attaque critique ou non
        : return : Affiche un message ou attaque la victime
        """
        if self.attack_can_go_on(victim):

            if critical:
                damages = self.attack
                self.attack_victim(victim, damages, True)

            else:
                damages = self.attack - victim.defense
                self.attack_victim(victim, damages, False)
