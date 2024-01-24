from Program.Entities.Entity import Entity


class Warrior(Entity):
    def __init__(self, id, name, category, attack, defense, life, critical_hit, initiative, parade):
        super().__init__(id, name, category, attack, defense, life, critical_hit, initiative)
        self.__parade = parade

    @property
    def parade(self):
        return self.__parade

    def print_info(self):
        """
        Affiche les informations sur le joueur
        """
        return f"Name: {self.name}\nCategory: Warrior\nAttack: {self.attack}\nDefense: {self.defense}\nLife: {self.life}\nCritical Hit: {self.critical_hit}% chance\nParade: {self.parade}% chance\nInitiative: {self.initiative}\n"
