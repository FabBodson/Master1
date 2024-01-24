from random import randint, choice
import threading
from Program.Functions import Players_and_Teams
from Program.Entities.Team import Team
import Program.Functions.Tactics as Tactics
import sqlite3

lock = threading.Lock()


def game_can_go_one(teamA, teamB):
    """
    Vérifie si le match peut continuer ou non en retournant faux lorsque l'une des deux équipe n'a plus de membre.
    : param teamA : [Objet Team] Première équipe.
    :param teamB: [Objet Team] Deuxième équipe.
    :return: Booleen
    """

    if teamA.size == 0 or teamB.size == 0:
        return False

    return True


def insert_new_game(teamA_tactic, teamB_tactic):
    """
    Ajout d'une entrée dans la DB pour le match.
    : param teamA_tactic : Attribut de l'objet Team décrivant la tactique utilisée par l'équipe A
    : param teamB_tactic : Attribut de l'objet Team décrivant la tactique utilisée par l'équipe B
    : return : l'ID de la partie en BD
    """
    db = sqlite3.connect('game.db')
    cursor = db.cursor()

    insert_game = "INSERT INTO Games (Winner, Loser, TeamA_tactic, TeamB_tactic) VALUES (?, ?, ?, ?)"
    cursor.execute(insert_game, ("NULL", "NULL", teamA_tactic, teamB_tactic))
    db.commit()

    cursor.execute("SELECT * FROM Games ORDER BY Game_ID DESC LIMIT 1")
    game_id = cursor.fetchone()[0]

    db.close()

    return game_id


def insert_game_player(game_id):
    """
    Ajoute les joueurs qui jouent pour cette partie.
    : param game_id : ID de l'entrée en BD de la partie
    """
    db = sqlite3.connect('game.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Players WHERE is_selected = 1")
    players = cursor.fetchall()

    insert_player = "INSERT INTO Game_players (Player_ID, Game_ID) VALUES (?, ?)"
    for player in players:
        cursor.execute(insert_player, (player[0], game_id))
        db.commit()

    db.close()


def insert_alive_players(game_id):
    """
    Ajoute les joueurs encore vivants pour cette partie.
    : param game_id : ID de l'entrée en BD de la partie
    """
    db = sqlite3.connect('game.db')
    cursor = db.cursor()

    cursor.execute("SELECT * FROM Players WHERE is_alive = 1 AND is_selected = 1")
    players = cursor.fetchall()

    insert_player = "INSERT INTO Players_alive (Player_ID, Game_ID) VALUES (?, ?)"
    for player in players:
        cursor.execute(insert_player, (player[0], game_id))
        db.commit()

    db.close()


def matchmaking():
    """
    Crée les 20 joueurs en BD, crée les deux équipes qui vont sélectionner chacune leurs membres.
    Ensuite, crée les entrées dans la BD qui correspondent à ce nouveau match.
    : return : Les deux objets Team
    """

    for _ in range(20):
        Players_and_Teams.create_user_in_db()

    print("\n-------------------")
    teamA = Team("Team A")
    teamA.select_members()
    teamA.select_tactic()
    teamA.print_info()

    print("\n-------------------")
    teamB = Team("Team B")
    teamB.select_members()
    teamB.select_tactic()
    teamB.print_info()

    # CREATE DB GAME
    game_id = insert_new_game(teamA.tactic[0], teamB.tactic[0])

    # CREATE DB GAME_PLAYERS
    insert_game_player(game_id)

    # CREATE DB PLAYERS_ALIVE
    insert_alive_players(game_id)

    return teamA, teamB


def normal_fight(attacker, defender, att_team, def_team):
    """
    Scénario du combat.
    :param attacker: [Objet Entité] Attaquant
    :param defender: [Objet Entité] Défenseur
    :param att_team: [Objet Team] Equipe attaquant
    : param def_team : [Objet Team] Equipe qui défend
    : return : Des messages sur le déroulement du combat
    """
    # Check si les deux sont toujours bien en vie
    if attacker.is_alive() and defender.is_alive():
        # Check s'ils sont en train de se battre ou non
        if attacker.is_fighting or defender.is_fighting:
            print("\nThey are already fighting !\n")
        else:
            # Etat en combat
            attacker.is_fighting = True
            defender.is_fighting = True

            print(f"---------\nAttacker:\n---------\n{att_team.name}\n{attacker.print_info()}")
            print(f"---------\nDefender:\n---------\n{def_team.name}\n{defender.print_info()}")

            # Check si l'attaque se fait en coup critique ou non
            if randint(1, 100) <= attacker.critical_hit:
                critical = True
                print("-------------------\nAttack information:\n-------------------")

                attacker.use_attack_on(defender, critical)

            else:
                critical = False
                # Check si l'attaque peut attaquer ou bien s'il est trop faible
                if attacker.attack < defender.defense:
                    # Si attaque plus faible que la défense adverse, aucun dégat infligé
                    print("-----------------------------------------")
                    print("Equity: attacker is too weak for defender")
                    print("-----------------------------------------")
                else:
                    print("-------------------\nAttack information:\n-------------------")
                    attacker.use_attack_on(defender, critical)

            if defender.is_alive() is False:
                def_team.remove_member(defender)

            attacker.is_fighting = False
            defender.is_fighting = False
    # L'un des deux est mort
    else:
        print(f"\nNo attack. One of them is dead !")


def fight(att_team, def_team):
    """
    Scénario du combat principal.
    :param att_team: [Objet Team] Equipe attaquant
    : param def_team : [Objet Team] Equipe qui défend
    : return : Des messages sur le déroulement du combat
    """
    # Blocage des ressources
    lock.acquire()
    if game_can_go_one(att_team, def_team):
        print("\n################ New duel ################\n")

        attacker = choice(att_team.members)
        attacking_tactic = att_team.tactic[0]
        print("Tactic :")

        # Attaquer les Healer en premier
        if attacking_tactic == 1:
            print("Attack Healers first")
            healers = Tactics.get_healers(def_team)

            if len(healers) == 0:
                defender = choice(def_team.members)
            else:
                defender = choice(healers)

        # Attaque random
        elif attacking_tactic == 2:
            print("Attack random")
            defender = choice(def_team)

        # Attaque le plus faible
        elif attacking_tactic == 3:
            print("Attack weakest")
            defender = Tactics.get_weakest_adversary(def_team)

        # Attaque la catégorie la moins représentée
        else:
            print("Attack least represented category")
            least_represented = Tactics.get_least_represented_cat(def_team)

            if len(least_represented) == 0:
                defender = choice(def_team.members)

            else:
                defender = choice(least_represented)

        normal_fight(attacker, defender, att_team, def_team)

    lock.release()


def unselect_users_db(team):
    """
    Permet de libérer les joueurs encore vivants repris pour la partie afin qu'ils soient sélectionnables plus tard.
    :param team: [Objet Team] Equipe qui a encore des membres
    """
    for member in team.members:
        team.remove_member(member)

