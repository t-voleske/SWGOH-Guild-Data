import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


password = os.getenv('PASS')
host = os.getenv('HOST')
user = os.getenv('USER')


pg_connection_dict = {
    'dbname': 'guild_data',
    'user': user,
    'password': password,
    'port': 5432,
    'host': host
}


def enter_players(players_to_insert):

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Entering player data into DB...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            # Insert multiple books at once
            cur.executemany(
                "INSERT INTO players (player_id, nickname, total_gp, guild_id, last_activity_time) VALUES (%s, %s, %s, %s, %s);",
                players_to_insert,
            )
            print("Inserted player data")

            # Commit the changes to the database
            conn.commit()
            print("Done")

    except Exception as e:
        print("Connection failed.")
        print(e)

# Data to be inserted
#player_arr = [("ZjPDOjUFTemxd-qtzP9u4w", "Gametye", 3389079, "Xyw6K1R1SOazMbS94TX7fw"),("B1PcmWS6QIysLlMjtEXR2Q", "Masterscott149", 10863946, "Xyw6K1R1SOazMbS94TX7fw"),("57PvGBQzTtWZ9kR1wJY4lA", "Mölli", 11198417, "Xyw6K1R1SOazMbS94TX7fw"),]
#enter_players(player_arr)


def log_gp(gp_logs):

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Logging player GP ...')
        conn = psycopg2.connect(**pg_connection_dict)


            # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Insert multiple books at once
            cur.executemany(
                "INSERT INTO gp_history (player_id, total_gp, timestamp) VALUES (%s, %s, %s);",
                gp_logs,
            )
            print("Inserted gp_history")

            # Commit the changes to the database
            conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)

def enter_player_check(player_checks):

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Entering player checks into DB...')
        conn = psycopg2.connect(**pg_connection_dict)


        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Insert multiple values at once
            cur.executemany(
                "INSERT INTO players_roster_checks (all_jkck_reqs_7_star, jkck_unlocked, jkck_r7, cere_r7, jkck_skill_levels_done, player_id) VALUES (%s, %s, %s, %s, %s, %s);",
                player_checks,
            )
            print("Inserted into players_roster_checks")

            # Commit the changes to the database
            conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)

def enter_tickets(tkts):

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Logging tickets...')
        conn = psycopg2.connect(**pg_connection_dict)


        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Insert multiple values at once
            cur.executemany(
                "INSERT INTO ticket_log (player_id, created_at, tickets_lost) VALUES (%s, %s, %s);",
                tkts,
            )
            print("Inserted ticket_logs")

            # Commit the changes to the database
            conn.commit()

    except Exception as e:
        print("Connection failed to ticket_log.")
        print(e)

def enter_log_raid_score(raid_score_logs):

    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Logging raid score...')
        conn = psycopg2.connect(**pg_connection_dict)


        # Open a cursor to perform database operations
        with conn.cursor() as cur:
            # Insert multiple values at once
            cur.executemany(
                "INSERT INTO raid_score_log (player_id, raid_score, percent_of_avg) VALUES (%s, %s, %s);",
                raid_score_logs,
            )
            print("Inserted raid_score_log")

            # Commit the changes to the database
            conn.commit()

    except Exception as e:
        print("Connection failed to ticket_log.")
        print(e)