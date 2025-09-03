import os
import psycopg2
from dotenv import load_dotenv
from helper_functions import check_none


load_dotenv()
password: str = check_none(
    os.getenv("PASS"), "Error: Check .env file. PASS should not be None"
)
host: str = check_none(
    os.getenv("HOST"), "Error: Check .env file. HOST should not be None"
)
user: str = check_none(
    os.getenv("USER"), "Error: Check .env file. USER should not be None"
)
db_name: str = check_none(
    os.getenv("DBNAME"), "Error: Check .env file. DBNAME should not be None"
)
port: int = int(
    check_none(os.getenv("PORT"), "Error: Check .env file. PORT should not be None")
)

pg_connection_dict = {
    "dbname": db_name,
    "user": user,
    "password": password,
    "port": port,
    "host": host,
}

# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------


def remove_from_guild(player_string: str):
    string: str = player_string
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        print("Removing from SON...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET guild_id = %s WHERE nickname = %s ;", (" ", string)
            )
            print("Updated player " + string)

            # Commit the changes
            conn.commit()

    except psycopg2.DatabaseError as e:
        print("Connection failed on remove_from_guild")
        print(e)
    finally:
        if conn:
            conn.close()


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------


def update_activity(activity_time, pid_str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        print("Updating activity in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                ("UPDATE players SET last_activity_time = %s WHERE player_id = %s ;"),
                (activity_time, pid_str),
            )

            # Commit the changes
            conn.commit()

    except psycopg2.DatabaseError as e:
        print("Connection failed in update_activity.")
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
        print("Updating GP in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET total_gp = %s WHERE player_id = %s ;", (gp, pId_str)
            )

            # Commit the changes
            conn.commit()

    except psycopg2.DatabaseError as e:
        print("Connection failed to update total_gp")
        print(e)
    finally:
        if conn:
            conn.close()


def updateLastRaidResult(last_raid_result, pid_str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        print("Updating last raid result in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET last_raid_result = %s WHERE player_id = %s ;",
                (last_raid_result, pid_str),
            )

            # Commit the changes
            conn.commit()

    except psycopg2.DatabaseError as e:
        print("Connection failed to update last_raid_result.")
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
        print("Updating roster checks in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players_roster_checks SET all_jkck_reqs_7_star = %s,"
                " jkck_unlocked = %s, jkck_r7 = %s, cere_r7 = %s,"
                " jkck_skill_levels_done = %s WHERE player_id = %s ;",
                player_checks,
            )

            # Commit the changes
            conn.commit()

    except psycopg2.DatabaseError as e:
        print("Connection failed to update players_roster_checks")
        print(e)
    finally:
        if conn:
            conn.close()
