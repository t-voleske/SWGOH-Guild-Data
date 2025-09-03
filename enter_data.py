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


def enter_players(players_to_insert):
    conn = None
    try:
        print("Entering new player data into players table...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players (player_id, nickname, total_gp, guild_id, last_activity_time) VALUES (%s, %s, %s, %s, %s);",
                players_to_insert,
            )
            print("Inserted players data")

            conn.commit()
            print("Done")

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def enter_gp_logs(gp_logs):
    conn = None
    try:
        print("Logging player GP ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO gp_history (player_id, total_gp, timestamp) VALUES (%s, %s, NOW());",
                gp_logs,
            )
            print("Inserted gp_history")

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


def enter_player_check(player_checks):
    conn = None
    try:
        print("Entering player checks into player_roster_checks table ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players_roster_checks (all_jkck_reqs_7_star, jkck_unlocked, jkck_r7, cere_r7, jkck_skill_levels_done, player_id) VALUES (%s, %s, %s, %s, %s, %s);",
                player_checks,
            )
            print("Inserted into players_roster_checks")
            conn.commit()

    except Exception as e:
        print("Connection failed.")
        print(e)
    finally:
        if conn:
            conn.close()


def enter_tickets(tickets):
    conn = None
    try:
        print("Logging tickets ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO ticket_log (player_id, created_at, tickets_lost) VALUES (%s, NOW(), %s);",
                tickets,
            )
            print("Inserted ticket_logs")
            conn.commit()

    except Exception as e:
        print("Connection failed to ticket_log.")
        print(e)
    finally:
        if conn:
            conn.close()


def enter_raid_score_log(raid_score_logs):
    conn = None
    try:
        print("Logging raid score...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO raid_score_log (player_id, raid_score, percent_of_avg) VALUES (%s, %s, %s);",
                raid_score_logs,
            )
            print("Inserted raid_score_log")
            conn.commit()

    except Exception as e:
        print("Connection failed to ticket_log.")
        print(e)
    finally:
        if conn:
            conn.close()


def enter_player_archive(players_to_insert):
    if not players_to_insert:
        print("No players to insert.")
        return

    conn = None
    try:
        print(f"Entering {len(players_to_insert)} new players into players table...")
        conn = psycopg2.connect(**pg_connection_dict)
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players_archive (player_id, nickname, total_gp, guild_id) VALUES (%s, %s, %s, %s);",
                players_to_insert,
            )
            inserted_count = cur.rowcount
            print(f"Inserted {inserted_count} players data")
            conn.commit()
            print("Done")
    except psycopg2.IntegrityError as ie:
        print(f"Data integrity error (duplicate keys, constraint violations): {ie}")
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
