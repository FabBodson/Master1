from Program.Functions import Game
from Program.SQL.create_db import create_db
import threading


def main():
    # Création de la base de données
    create_db("game.db")

    # Création des joueurs et des équipes
    teamA, teamB = Game.matchmaking()

    print(f"\n--- BEGINNING OF THE GAME ---\n")

    try:
        while True:

            # Vérification de l'état de la partie, si on peut continuer ou non
            if not Game.game_can_go_one(teamA, teamB):
                break

            # Création des threads pour chaque joueur, qui va se battre contre l'autre.
            p1 = threading.Thread(target=Game.fight, args=(teamA, teamB))
            p2 = threading.Thread(target=Game.fight, args=(teamB, teamA))

            p1.start()
            p2.start()

            p1.join()
            p2.join()

    except IndexError:
        pass

    finally:
        print(f"\n\n--- END OF THE GAME ---")

        if teamB.size == 0:
            print("\n#####################")
            print("### TeamA has won ###")
            teamA.print_info()
            print("#####################")
            Game.unselect_users_db(teamA)

        if teamA.size == 0:
            print("\n#####################")
            print("### TeamB has won ###")
            teamB.print_info()
            print("#####################")
            Game.unselect_users_db(teamB)


if __name__ == '__main__':
    main()
