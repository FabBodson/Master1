from Program.Entities.Entity import Entity


class Magus(Entity):
    def __init__(self, id, name, category, attack, defense, life, critical_hit, initiative):
        super().__init__(id, name, category, attack, defense, life, critical_hit, initiative)

    def print_info(self):
        """
        Affiche les informations sur le joueur
        """
        return f"Name: {self.name}\nCategory: Magus\nAttack: {self.attack}\nDefense: {self.defense}\nLife: {self.life}\nCritical Hit: {self.critical_hit}% chance\nInitiative: {self.initiative}\n"
