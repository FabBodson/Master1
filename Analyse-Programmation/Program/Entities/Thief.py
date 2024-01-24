from Program.Entities.Entity import Entity


class Thief(Entity):
    def __init__(self, id, name, category, attack, defense, life, critical_hit, initiative, dodge):
        super().__init__(id, name, category, attack, defense, life, critical_hit, initiative)
        # Esquive
        self.__dodge = dodge

    @property
    def dodge(self):
        return self.__dodge

    @dodge.setter
    def dodge(self, value):
        self.__dodge = value

    def print_info(self):
        """
        Affiche les informations sur le joueur
        """
        return f"Name: {self.name}\nCategory: Thief\nAttack: {self.attack}\nDefense: {self.defense}\nLife: {self.life}\nCritical Hit: {self.critical_hit}% chance\nDodge: {self.dodge}% chance\nInitiative: {self.initiative}\n"
