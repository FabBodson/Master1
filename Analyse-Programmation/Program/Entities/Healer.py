from Program.Entities.Entity import Entity


class Healer(Entity):
    def __init__(self, id, name, category, attack, defense, life, critical_hit, initiative, parade, heal):
        super().__init__(id, name, category, attack, defense, life, critical_hit, initiative)
        self.heal = heal
        self.__parade = parade

    @property
    def parade(self):
        return self.__parade

    def print_info(self):
        """
        Affiche les informations sur le joueur
        """
        return f"Name: {self.name}\nCategory: Healer\nAttack: {self.attack}\nDefense: {self.defense}\nLife: {self.life}\nCritical Hit: {self.critical_hit}% chance\nParade: {self.parade}% chance\nInitiative: {self.initiative}\nHeal: {self.heal}\n"

    def use_heal_on(self, teammate):
        """
        Applique la capacité de soin
        : param teammate : [Objet Entité] Coéquipier à soigner
        : return : Affiche un message
        """
        if teammate.original_life == teammate.life:
            print(f"All the teammates have a full life ! No one was healed.")
        else:
            old_life = teammate.life
            teammate.life = teammate.life + self.heal
            print(f"Teammate {teammate.name} the {teammate.category} was healed by {self.name} the {self.category} !\nLife went from {old_life} to {teammate.life}")

    def self_heal(self):
        """
        Se soigne tout seul.
        """
        print(f"Healer healed himself. His life was: {self.life}")
        self.life += round(self.original_life * 0.20)
        print(f"Now his life is: {self.life}")
