import logging
import psycopg2
from .helper_functions import get_env, setup_logging

logger = logging.getLogger("guild_data_app")
setup_logging()

def setup_connection():
    """
    Set up psql connection dict with params from .env file
    """
    password: str = get_env("PASS")
    host: str = get_env("HOST")
    user: str = get_env("USER")
    db_name: str = get_env("DBNAME")
    port: int = int(get_env("PORT"))

    connection_dict = {
        "dbname": db_name,
        "user": user,
        "password": password,
        "port": port,
        "host": host,
    }
    return connection_dict


def remove_from_guild(player_id: str):
    """
    Remove guild_id from a player record to update guild affiliation status
    """
    pg_connection_dict = setup_connection()
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
    """
    Update the last activity time for a player
    """
    pg_connection_dict = setup_connection()
    conn = None
    try:
        # read the connection parameters

        # connect to the PostgreSQL server
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
    """
    Update the current total GP for a player
    """
    pg_connection_dict = setup_connection()
    conn = None
    try:

        # connect to the PostgreSQL server
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
    """
    Update the last raid result for a player
    """
    pg_connection_dict = setup_connection()
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
    """
    Update the roster check entry for a player
    """
    pg_connection_dict = setup_connection()
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
                "UPDATE players_roster_checks SET reva_ready = %s,"
                " gi_r7 = %s, bkm_r7 = %s,"
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
