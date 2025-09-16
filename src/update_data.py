import logging
import psycopg2
from src.helper_functions import get_env, setup_logging

logger = logging.getLogger("guild_data_app")
setup_logging()

password: str = get_env("PASS")
host: str = get_env("HOST")
user: str = get_env("USER")
db_name: str = get_env("DBNAME")
port: int = int(get_env("PORT"))

pg_connection_dict = {
    "dbname": db_name,
    "user": user,
    "password": password,
    "port": port,
    "host": host,
}


def remove_from_guild(player_id: str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        logger.info("Removing from SON...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET guild_id = %s WHERE nickname = %s ;",
                (" ", player_id),
            )
            logger.info("Updated player: %s", player_id)

            # Commit the changes
            conn.commit()

    except psycopg2.IntegrityError as ie:
        logger.error(
            "Data integrity error (duplicate keys, constraint violations): %s", ie
        )
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def update_activity(activity_time, player_id: str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        logger.info("Updating activity in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                ("UPDATE players SET last_activity_time = %s WHERE player_id = %s ;"),
                (activity_time, player_id),
            )

            # Commit the changes
            conn.commit()

    except psycopg2.IntegrityError as ie:
        logger.error(
            "Data integrity error (duplicate keys, constraint violations): %s", ie
        )
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def updateGP(gp, player_id: str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        logger.info("Updating GP in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET total_gp = %s WHERE player_id = %s ;",
                (gp, player_id),
            )

            # Commit the changes
            conn.commit()

    except psycopg2.IntegrityError as ie:
        logger.error(
            "Data integrity error (duplicate keys, constraint violations): %s", ie
        )
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def updateLastRaidResult(last_raid_result, player_id: str):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        logger.info("Updating last raid result in DB...")
        conn = psycopg2.connect(**pg_connection_dict)
        # Open a cursor to perform database operations

        with conn.cursor() as cur:
            # Update a data row in the table
            cur.execute(
                "UPDATE players SET last_raid_result = %s WHERE player_id = %s ;",
                (last_raid_result, player_id),
            )

            # Commit the changes
            conn.commit()

    except psycopg2.IntegrityError as ie:
        logger.error(
            "Data integrity error (duplicate keys, constraint violations): %s", ie
        )
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()


def updateRosterChecks(player_checks):
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
        logger.info("Updating roster checks in DB...")
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

    except psycopg2.IntegrityError as ie:
        logger.error(
            "Data integrity error (duplicate keys, constraint violations): %s", ie
        )
        if conn:
            conn.rollback()
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
