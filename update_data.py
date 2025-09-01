import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
password = os.getenv('PASS')
host = os.getenv('HOST')
user = os.getenv('USER')
db_name = os.getenv('DBNAME')
port = os.getenv('PORT')
if port is None:
    raise ValueError("Check .env file! PORT variable must not be None")
port = int(port)

pg_connection_dict = {
    'dbname': db_name,
    'user': user,
    'password': password,
    'port': port,
    'host': host
}

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def remove_son(str):
    string = str
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Removing from SON...')
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
                # Update a data row in the table
                cur.execute(
                    "UPDATE players SET guild_id = %s WHERE nickname = %s ;", (" ", string)
                )
                print("Updated player " + string)

                # Commit the changes
                conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def updateActivity(activity_time, pId_str):
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Updating activity in DB...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Update a data row in the table
                cur.execute(
                    "UPDATE players SET last_activity_time = %s WHERE player_id = %s ;", (activity_time, pId_str)
                )

                # Commit the changes
                conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def updateGP(gp, pId_str):
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Updating GP in DB...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Update a data row in the table
                cur.execute(
                    "UPDATE players SET total_gp = %s WHERE player_id = %s ;", (gp, pId_str)
                )

                # Commit the changes
                conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def updateLastRaidResult(last_raid_result, pId_str):
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Updating last raid result in DB...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Update a data row in the table
                cur.execute(
                    "UPDATE players SET last_raid_result = %s WHERE player_id = %s ;", (last_raid_result, pId_str)
                )

                # Commit the changes
                conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
def updateRosterChecks(player_checks):
    conn = None
    try:
        # read the connection parameters

         # connect to the PostgreSQL server
        print('Updating roster checks in DB...')
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
                # Update a data row in the table
                cur.execute(
                    "UPDATE players_roster_checks SET all_jkck_reqs_7_star = %s, jkck_unlocked = %s, jkck_r7 = %s, cere_r7 = %s, jkck_skill_levels_done = %s WHERE player_id = %s ;", player_checks
                )

                # Commit the changes
                conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()