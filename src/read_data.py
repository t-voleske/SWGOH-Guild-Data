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


def read_tickets_weekly(guild_id: str, order_str: str):
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
                "WHERE guild_id = %s "
                f"ORDER BY {order_str};",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def read_tickets_monthly(guild_id: str, order_str: str):
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
                "WHERE guild_id = %s "
                f"ORDER BY {order_str};",
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


def read_players_data(guild_id: str, order_str: str):
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
                f"ORDER BY {order_str};",
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


def read_member_points(guild_id: str, order_str: str):
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
                f"ORDER BY {order_str};",
                (guild_id,),
            )
            rows = cur.fetchall()
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def get_guild_from_nickname(nickname: str):
    conn = None
    try:
        logger.info("Getting guild from nickname...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT guild_name "
                "FROM guild "
                "WHERE guild_id = "
                "(SELECT guild_id FROM players WHERE nickname = %s);",
                (nickname,),
            )
            rows = cur.fetchall()
            if rows:
                return rows[0][0]
            else:
                return ""

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def get_last_tb_data(guild_id: str) -> list | None:
    conn = None
    try:
        logger.info("Getting data of latest TB for guild %s...", guild_id)
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT gm.nickname AS nickname, "
                "tbi.total_territory_points AS total_territory_points, "
                "tbi.total_waves_completed, tbi.total_missions_attempted, "
                "tbi.wave_completion_ratio AS wave_completion_ratio, "
                "tbi.phases_missed AS phases_missed, "
                "tbi.created_at AS created_at "
                "FROM guild_members gm "
                "LEFT JOIN players p "
                "ON gm.player_id = p.player_id "
                "LEFT JOIN tb_import tbi "
                "ON gm.nickname = tbi.nickname "
                "WHERE p.guild_id = %s AND "
                "tbi.created_at = (SELECT MAX(created_at) FROM tb_import) "
                "ORDER BY nickname DESC;",
                (guild_id,),
            )
            rows = cur.fetchall()
            if not rows:
                raise psycopg2.DataError
            return rows
    except psycopg2.DataError as e:
        logger.error(e)
        logger.debug(
            "Query returned no data. Check if there is data in tb_import for %s",
            guild_id,
        )
    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()


def get_last_tb_data_ordered(guild_id: str, order_str: str) -> list | None:
    conn = None
    try:
        logger.info("Getting data of latest TB for guild %s...", guild_id)
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.execute(
                "SELECT gm.nickname AS nickname, "
                "tbi.total_territory_points AS total_territory_points, "
                "tbi.total_waves_completed AS total_waves_completed, "
                "tbi.total_missions_attempted AS total_missions_attempted, "
                "tbi.wave_completion_ratio AS wave_completion_ratio, "
                "tbi.phases_missed AS phases_missed, "
                "tbi.created_at AS created_at "
                "FROM guild_members gm "
                "LEFT JOIN players p "
                "ON gm.player_id = p.player_id "
                "LEFT JOIN tb_import tbi "
                "ON gm.nickname = tbi.nickname "
                "WHERE p.guild_id = %s AND "
                "tbi.created_at = (SELECT MAX(created_at) FROM tb_import) "
                f"ORDER BY {order_str};",
                (guild_id,),
            )
            rows = cur.fetchall()
            if not rows:
                raise psycopg2.DataError
            return rows
    except psycopg2.DataError as e:
        logger.error(e)
        logger.debug(
            "Query returned no data. Check if there is data in tb_import for %s",
            guild_id,
        )
    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
    finally:
        if conn:
            conn.close()
