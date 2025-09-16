import logging
import psycopg2
from src.helper_functions import setup_logging, get_env

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


def remove_from_players(players_to_remove):
    if not players_to_remove:
        logger.info("No players to remove.")
        return

    conn = None
    try:
        logger.info("Removing %s old guild members...", len(players_to_remove))
        conn = psycopg2.connect(**pg_connection_dict)
        with conn.cursor() as cur:
            cur.executemany(
                "DELETE FROM players WHERE player_id = %s;",
                players_to_remove,
            )
            deleted_count = cur.rowcount
            logger.info("Removed %s old guild members", deleted_count)
            conn.commit()
            logger.info("Done")
    except psycopg2.Error as db_error:
        logger.error("Database error: %s", db_error)
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
