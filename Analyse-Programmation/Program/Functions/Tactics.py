def get_healers(def_team):
    """
    Sélectionner les Healer de l'équipe adverse
    : param def_team : [Objet Team] Equipe adverse
    : return : [list] liste des Healer de l'équipe adverse
    """
    healers = []
    for defender in def_team.members:
        if defender.category == "Healer":
            healers.append(defender)

    return healers


def get_weakest_adversary(def_team):
    """
    Sélectionne l'adversaire ayant le moins de vie
    : param def_team : [Objet Team] Equipe adverse
    : return : L'adversaire ayant le moins de vie
    """
    weakest = def_team.members[0]

    for member in def_team.members:
        if member.life <= weakest.life:
            weakest = member

    return weakest


def get_least_represented_cat(def_team):
    """
    Recherche la catégorie la moins représentée et retourne une liste avec les membres faisant partie de la catégorie
    : param def_team : [Objet Team] Equipe adverse
    : return : [list] liste avec les membres faisant partie de la catégorie la moins représentée
    """
    categories = {
        "Warrior": 0,
        "Thief": 0,
        "Magus": 0,
        "Healer": 0
    }

    for member in def_team.members:
        if member.category == "Warrior":
            categories["Warrior"] += 1

        elif member.category == "Thief":
            categories["Thief"] += 1

        elif member.category == "Magus":
            categories["Magus"] += 1
        else:
            categories["Healer"] += 1

    least_represented = min(categories, key=categories.get)

    category_members = []
    for defender in def_team.members:
        if defender.category == least_represented:
            category_members.append(defender)

    return category_members
