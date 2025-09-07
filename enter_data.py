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


def enter_players(players_to_insert):
    conn = None
    try:
        logger.info("Entering new player data into players table...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players "
                "(player_id, nickname, total_gp, guild_id, last_activity_time) "
                "VALUES (%s, %s, %s, %s, %s);",
                players_to_insert,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s players into players table", inserted_count)
            conn.commit()
            logger.info("Done")
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


def enter_gp_logs(gp_logs):
    conn = None
    try:
        logger.info("Logging player GP ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO gp_history "
                "(player_id, total_gp, timestamp) "
                "VALUES (%s, %s, NOW());",
                gp_logs,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s player GP logs", inserted_count)
            conn.commit()
            logger.info("Done")
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


def enter_player_check(player_checks):
    conn = None
    try:
        logger.info("Entering player checks into player_roster_checks table ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players_roster_checks "
                "(all_jkck_reqs_7_star, jkck_unlocked, "
                "jkck_r7, cere_r7, jkck_skill_levels_done, player_id) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                player_checks,
            )
            logger.info("Inserted into players_roster_checks")
            conn.commit()
            logger.info("Done")
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


def enter_tickets(tickets):
    conn = None
    try:
        logger.info("Logging tickets ...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO ticket_log "
                "(player_id, created_at, tickets_lost) "
                "VALUES (%s, NOW(), %s);",
                tickets,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s ticket logs", inserted_count)
            conn.commit()
            logger.info("Done")
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


def enter_raid_score_log(raid_score_logs):
    conn = None
    try:
        logger.info("Logging raid score...")
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO raid_score_log "
                "(player_id, raid_score, percent_of_avg) "
                "VALUES (%s, %s, %s);",
                raid_score_logs,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s raid score logs", inserted_count)
            conn.commit()
            logger.info("Done")
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


def enter_player_archive(players_to_insert):
    if not players_to_insert:
        logger.info("No players to insert.")
        return

    conn = None
    try:
        logger.info(
            "Entering %s new players into players table...", len(players_to_insert)
        )
        conn = psycopg2.connect(**pg_connection_dict)
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO players_archive "
                "(player_id, nickname, total_gp, guild_id) "
                "VALUES (%s, %s, %s, %s);",
                players_to_insert,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s players data", inserted_count)
            conn.commit()
            logger.info("Done")
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


def enter_tb_data(tb_data):
    if not tb_data:
        logger.warning("No TB data to insert")
        return

    conn = None
    try:
        logger.info(
            "Entering tb data about %s players into the tb_import table...",
            len(tb_data),
        )
        conn = psycopg2.connect(**pg_connection_dict)
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO tb_import "
                "(nickname, total_territory_points, total_waves_completed, total_missions_attempted, wave_completion_ratio, phases_missed) "
                "VALUES (%s, %s, %s, %s, %s, %s);",
                tb_data,
            )
            inserted_count = cur.rowcount
            logger.info("Inserted %s players data", inserted_count)
            conn.commit()
            logger.info("Done")
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
