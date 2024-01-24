import sqlite3

CREATE_TABLE_PLAYERS = "CREATE TABLE Players (Player_ID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR(255) NOT NULL, Category VARCHAR(255) NOT NULL, Attack INTEGER NOT NULL, Defense INTEGER NOT NULL, Life INTEGER NOT NULL, Critical_hit INTEGER NOT NULL, Initiative FLOAT NOT NULL, Original_life INTEGER NOT NULL, is_alive BIT NOT NULL, Dodge INTEGER, Parade INTEGER, Heal INTEGER, is_selected BIT NOT NULL)"

CREATE_TABLE_GAMES = "CREATE TABLE Games (Game_ID INTEGER PRIMARY KEY AUTOINCREMENT, Winner VARCHAR(255), Loser VARCHAR(255), TeamA_tactic VARCHAR(255), TeamB_tactic VARCHAR(255))"

CREATE_TABLE_GAME_PLAYERS = "CREATE TABLE Game_players (GamePlayer_ID INTEGER PRIMARY KEY AUTOINCREMENT, Player_ID INTEGER NOT NULL, Game_ID INTEGER NOT NULL)"

CREATE_TABLE_PLAYERS_ALIVE = "CREATE TABLE Players_alive (PlayerAlive_ID INTEGER PRIMARY KEY AUTOINCREMENT, Player_ID INTEGER NOT NULL, Game_ID INTEGER NOT NULL)"

CREATE_TABLE_TACTICS = "CREATE TABLE Tactics (Tactic_ID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR(255) NOT NULL)"

TACTIC1 = 'Attaque les Soigneurs en premiers'
TACTIC2 = 'Attaquer au hasard'
TACTIC3 = 'Attaquer ceux qui ont le moins de points de vies'
TACTIC4 = 'Attaquer la catégorie la moins représentée'


def create_db(db_file):
    """
    Se connecte à une base de donnée indiquée et exécute des requêtes afin de créer la BD.
    : param db_file : [str] Le fichier de base de données
    : return : Rien
    """
    try:
        create_queries = [CREATE_TABLE_PLAYERS, CREATE_TABLE_GAMES, CREATE_TABLE_GAME_PLAYERS,
                          CREATE_TABLE_PLAYERS_ALIVE, CREATE_TABLE_TACTICS]
        tactics = [TACTIC1, TACTIC2, TACTIC3, TACTIC4]

        db = sqlite3.connect(db_file)
        cursor = db.cursor()

        for query in create_queries:

            try:
                cursor.execute(query)
                query = query.split(" ")
                print(f"Table '{query[2]}' created.")
                db.commit()

            except Exception:
                query = query.split(" ")
                print(f"Table '{query[2]}' already created.")

        for tactic in tactics:
            insert_tactic = "INSERT INTO Tactics (name) VALUES (?)"
            cursor.execute(insert_tactic, (tactic,))
            db.commit()

        db.close()

    except FileNotFoundError:
        print("DataBase creation failed.")
