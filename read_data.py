import psycopg2
from helper_functions import get_env, setup_logging
import logging

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


def read_guild():
    conn = None
    try:
        logger.info("Reading from guild table...")
        conn = psycopg2.connect(**pg_connection_dict)
        logger.info(conn)
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM guild;")
            rows = cur.fetchall()

            logger.info("\n--- Guild ---")
            for row in rows:
                logger.info("guild_id: %s, guild_name: %s", row[0], row[1])
            logger.info("--------------------\n")
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_players_raw():
    conn = None
    try:
        logger.info("Reading all entries of players table")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM players ORDER BY nickname DESC;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_players(guild_id):
    conn = None
    try:
        logger.info("Reading from players table WHERE player part of guild")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "* FROM players "
                "WHERE guild_id::text = %s "
                "ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_roster_check():
    conn = None
    try:
        logger.info("Reading from players_roster_checks...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM players_roster_checks;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_tickets_weekly(guild_id):
    conn = None
    try:
        logger.info("Reading from tickets_aggregated_weekly view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "taw.nickname AS nickname, taw.tickets_lost AS tickets_lost, "
                "taw.days_tickets_lost AS days_tickets_lost, taw.full_days_lost AS full_days_lost "
                "FROM players p "
                "LEFT JOIN tickets_aggregated_weekly taw "
                "ON p.nickname = taw.nickname "
                "WHERE guild_id = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_tickets_monthly(guild_id):
    conn = None
    try:
        logger.info("Reading from tickets_aggregated_monthly view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "tam.nickname AS nickname, tam.tickets_lost AS tickets_lost, "
                "tam.days_tickets_lost AS days_tickets_lost, tam.full_days_lost AS full_days_lost "
                "FROM players p "
                "LEFT JOIN tickets_aggregated_monthly tam "
                "ON p.nickname = tam.nickname "
                "WHERE guild_id = %s ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


# Player level function. No multiple guild support needed
def read_zeffo_readiness():
    conn = None
    try:
        logger.info("Reading from zeffo_readiness view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM zeffo_readiness;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_guild_members(guild_id):
    conn = None
    try:
        logger.info("Reading from guild_members view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "* FROM guild_members "
                "WHERE guild_id::text = %s "
                "ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_last_login():
    conn = None
    try:
        logger.info("Reading from last_login table...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute("SELECT * FROM last_login;")
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_players_data(guild_id):
    conn = None
    try:
        logger.info("Reading from players_data table ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "* FROM players_data "
                "WHERE nickname IN "
                "(SELECT nickname FROM players WHERE guild_id = %s) "
                "ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_raid_performance_by_guild(guild_id):
    conn = None
    try:
        logger.info("Reading raid_performance view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "p.player_id, p.nickname, rp.score AS score, "
                "rp.percent_of_average AS percent_of_average "
                "FROM players p "
                "LEFT JOIN raid_performance rp "
                "ON p.nickname = rp.nickname WHERE guild_id::text = %s;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_member_points(guild_id):
    conn = None
    try:
        logger.info("Reading member_points view...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT "
                "* FROM member_points "
                "WHERE nickname IN "
                "(SELECT nickname FROM players WHERE guild_id = %s) "
                "ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()
