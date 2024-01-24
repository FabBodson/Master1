from random import randint, choice
import sqlite3


def get_name():
    """
    Crée un nom pour le joueur
    : return : [str] le nom du joueur
    """
    with open("Data/names.txt", "r") as names_file:
        names = names_file.readlines()
        return choice(names).rstrip()


def create_user_in_db():
    """
    Crée un joueur en BD
    """
    # Choix de la catégorie
    category = choice(("Warrior", "Thief", "Magus", "Healer"))
    name = get_name()

    # Connexion à la BD
    db = sqlite3.connect('game.db')
    cursor = db.cursor()

    # Création des attributs selon la catégorie du joueur puis insertion en BD
    if category is "Warrior":
        attack = randint(70, 90)
        defense = randint(70, 90)
        life = randint(120, 150)
        # % de chance
        critical_hit = randint(5, 7)
        initiative = randint(40, 60) / 1000
        parade = randint(40, 60)

        warrior = "INSERT INTO Players (Name, Category, Attack, Defense, Life, Critical_hit, Initiative, Original_life, is_alive, Dodge, Parade, Heal, is_selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(warrior, (name, category, attack, defense, life, critical_hit, initiative, life, 1, "NULL", parade, "NULL", 0))

    elif category is "Thief":
        attack = randint(40, 60)
        defense = randint(30, 50)
        life = randint(70, 80)
        # % de chance
        critical_hit = randint(15, 20)
        initiative = randint(75, 90) / 1000
        dodge = randint(40, 70)

        thief = "INSERT INTO Players (Name, Category, Attack, Defense, Life, Critical_hit, Initiative, Original_life, is_alive, Dodge, Parade, Heal, is_selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(thief, (name, category, attack, defense, life, critical_hit, initiative, life, 1, dodge, "NULL", "NULL", 0))

    elif category is "Magus":
        attack = randint(100, 150)
        defense = randint(20, 40)
        life = randint(60, 70)
        # % de chance
        critical_hit = randint(5, 7)
        initiative = randint(60, 70) / 1000

        magus = "INSERT INTO Players (Name, Category, Attack, Defense, Life, Critical_hit, Initiative, Original_life, is_alive, Dodge, Parade, Heal, is_selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(magus, (name, category, attack, defense, life, critical_hit, initiative, life, 1, "NULL", "NULL", "NULL", 0))

    else:
        attack = randint(30, 60)
        defense = randint(60, 80)
        life = randint(70, 90)
        # % de chance
        critical_hit = randint(5, 7)
        initiative = randint(50, 60) / 1000
        heal = round(defense / 4)
        parade = randint(50, 60)

        healer = "INSERT INTO Players (Name, Category, Attack, Defense, Life, Critical_hit, Initiative, Original_life, is_alive, Dodge, Parade, Heal, is_selected) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        cursor.execute(healer, (name, category, attack, defense, life, critical_hit, initiative, life, 1, "NULL", parade, heal, 0))

    db.commit()
    db.close()


def create_team(size):
    """
    Création de l'équipe en y ajoutant des membres selon la taille de l'équipe
    : param size : [int] Taille de l'équipe
    :return : [list] Liste des membres de l'équipe
    """
    # return requete DB
    team = []
    for _ in range(size):
        team.append(create_user_in_db())
    return team


def select_teammate_to_heal(team):
    """
    Choix d'un coéquipier à soigner
    :param team : [list] Liste des membres de l'équipe
    : return : Le coéquipier à soigner
    """
    if len(team) > 1:
        teammate = choice(team)
        # Si le coéquipier a perdu de la vie alors il est sélectionné
        if teammate.original_life > teammate.life:
            return teammate
        # S'il n'a pas perdu de vie alors on passe au suivant
        else:
            team.remove(teammate)
            return select_teammate_to_heal(team)
    else:
        return team[0]
