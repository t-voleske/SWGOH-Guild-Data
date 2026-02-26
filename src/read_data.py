import logging
import psycopg2
from .helper_functions import get_env, setup_logging



logger = logging.getLogger("guild_data_app")
setup_logging()


def setup_connection() -> dict:
    """
    Set up psql connection dict with params from .env file
    """
    password : str = get_env("PASS")
    host : str = get_env("HOST")
    user : str = get_env("USER")
    db_name : str = get_env("DBNAME")
    port : int = int(get_env("PORT"))

    connection_dict : dict = {
        "dbname": db_name,
        "user": user,
        "password": password,
        "port": port,
        "host": host,
    }
    return connection_dict

def get_valid_order_parameter(order_param: str) -> str:
    """
    Validate given order param from spreadsheet against whitelist to prevent SQL injection
    """
    valid_orders : dict = {
        'nickname ASC': 'nickname ASC',
        'nickname DESC': 'nickname DESC',
        'score_difference ASC': 'score_difference ASC',
        'score_difference DESC': 'score_difference DESC',
        'last_raid_result ASC': 'last_raid_result ASC',
        'last_raid_result DESC': 'last_raid_result DESC',
        'total_gp ASC': 'total_gp ASC',
        'total_gp DESC': 'total_gp DESC',
        'raid_score ASC': 'raid_score ASC',
        'raid_score DESC': 'raid_score DESC',
        'average_percent ASC': 'average_percent ASC',
        'average_percent DESC': 'average_percent DESC',
        'zeffo_ready ASC': 'zeffo_ready ASC',
        'zeffo_ready DESC': 'zeffo_ready DESC',
        'tickets_lost_week ASC': 'tickets_lost_week ASC',
        'tickets_lost_week DESC': 'tickets_lost_week DESC',
        'total_points ASC': 'total_points ASC',
        'total_points DESC': 'total_points DESC',
        'last_activity_p ASC': 'last_activity_p ASC',
        'last_activity_p DESC': 'last_activity_p DESC',
        'average_percent_p ASC': 'average_percent_p ASC',
        'average_percent_p DESC': 'average_percent_p DESC',
        'zero_raid_score ASC': 'zero_raid_score ASC',
        'zero_raid_score DESC': 'zero_raid_score DESC',
        'tickets_weekly ASC': 'tickets_weekly ASC',
        'tickets_weekly DESC': 'tickets_weekly DESC',
        'tickets_lost ASC': 'tickets_lost ASC',
        'tickets_lost DESC': 'tickets_lost DESC',
        'days_tickets_lost ASC': 'days_tickets_lost ASC',
        'days_tickets_lost DESC': 'days_tickets_lost DESC',
        'full_days_lost ASC': 'full_days_lost ASC',
        'full_days_lost DESC': 'full_days_lost DESC',
        'total_territory_points ASC': 'total_territory_points ASC',
        'total_territory_points DESC': 'total_territory_points DESC',
        'total_waves_completed ASC': 'total_waves_completed ASC',
        'total_waves_completed DESC': 'total_waves_completed DESC',
        'total_missions_completed ASC': 'total_missions_completed ASC',
        'total_missions_completed DESC': 'total_missions_completed DESC',
        'wave_completion_ratio ASC': 'wave_completion_ratio ASC',
        'wave_completion_ratio DESC': 'wave_completion_ratio DESC',
        'phases_missed ASC': 'phases_missed ASC',
        'phases_missed DESC': 'phases_missed DESC'
}
    if order_param not in valid_orders:
        logger.warning("Invalid order parameter: %s", order_param)
    return valid_orders.get(order_param, 'nickname ASC')

def get_valid_timeframe_parameter(timeframe_param: str) -> str:
    """
    Validate given timeframe from spreadsheet against whitelist to prevent SQL injection
    """
    valid_timeframes = {
        'two_weeks': 'two_weeks',
        'month': 'month'
}
    if timeframe_param not in valid_timeframes:
        logger.warning("Invalid order parameter: %s", timeframe_param)
    return valid_timeframes.get(timeframe_param, 'nickname ASC')


def make_sql_query_single(sql_query_str: str, query_source: str, sql_tuple: tuple | None = None) -> list:
    """
    Make a sql query to psql DB
    """
    pg_connection_dict = setup_connection()
    conn = None
    try:
        logger.info("Getting guild from %s...", query_source)
        conn = psycopg2.connect(**pg_connection_dict)

        with conn.cursor() as cur:
            if sql_tuple:
                logger.info("tuple: %s", sql_tuple)
                cur.execute(
                    sql_query_str,
                    sql_tuple
                )
            else:
                cur.execute(
                    sql_query_str
                )
            rows = cur.fetchall()
            if not rows:
                logger.warning("Query returned no data. Check if there is data in %s table or query is malformed", query_source)
                return []
            return rows

    except psycopg2.Error as e:
        logger.debug("Connection failed: %s", e)
        return []
    finally:
        if conn:
            conn.close()


def read_guild() -> list[tuple] | list:
    """
    Get the list of guilds and their data from guild table
    """
    query_str: str = "SELECT * FROM guild;"
    query_return: list = make_sql_query_single(query_str, "guild")
    return query_return


def read_players_raw() -> list[tuple] | list:
    """
    Get all data from players on all players in DB
    """
    query_str: str = "SELECT * FROM players ORDER BY nickname DESC;"
    query_return: list = make_sql_query_single(query_str, "players")
    return query_return


def read_players(guild_id) -> list:
    """
    Get all data from players for guild_id
    """
    query_str: str = "SELECT * FROM players WHERE guild_id::text = %s ORDER BY nickname DESC;"
    query_source: str = "players"
    query_tuple: tuple = (guild_id, )
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return



def read_roster_check() -> list:
    """
    Get the players_roster_checks view for everyone in the DB
    """
    query_str: str = "SELECT * FROM players_roster_checks;"
    query_source: str = "players_roster_checks"
    query_return: list = make_sql_query_single(query_str, query_source)
    return query_return


def read_tickets_weekly(guild_id: str, order_str: str) -> list:
    """
    Get the weekly accumulated ticket violations for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
        "SELECT "
        "taw.nickname AS nickname, taw.tickets_lost AS tickets_lost, "
        "taw.days_tickets_lost AS days_tickets_lost, taw.full_days_lost AS full_days_lost "
        "FROM players p "
        "LEFT JOIN tickets_aggregated_weekly taw "
        "ON p.nickname = taw.nickname "
        "WHERE guild_id = %s "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "tickets_aggregated_weekly"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_tickets_monthly(guild_id: str, order_str: str) -> list:
    """
    Get the monthly accumulated ticket violations for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
        "SELECT "
        "tam.nickname AS nickname, tam.tickets_lost AS tickets_lost, "
        "tam.days_tickets_lost AS days_tickets_lost, tam.full_days_lost AS full_days_lost "
        "FROM players p "
        "LEFT JOIN tickets_aggregated_monthly tam "
        "ON p.nickname = tam.nickname "
        "WHERE guild_id = %s "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "tickets_aggregated_weekly"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_last_login() -> list:
    """
    Get the last_logins for guild_id
    """
    query_str: str = "SELECT * FROM last_login;"
    query_source: str = "last_login"
    query_return: list = make_sql_query_single(query_str, query_source)
    return query_return


def read_players_data(guild_id: str, order_str: str) -> list:
    """
    Get the players_data view for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
        "SELECT "
        "* FROM players_data "
        "WHERE nickname IN "
        "(SELECT nickname FROM players WHERE guild_id = %s) "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "players"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_players_data_full_rote(guild_id: str, order_str: str) -> list:
    """
    Get the players_data_full_rote view for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
        "SELECT "
        "* FROM players_dataplayers_data_full_rote "
        "WHERE nickname IN "
        "(SELECT nickname FROM players WHERE guild_id = %s) "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "players"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_raid_performance_by_guild(guild_id) -> list:
    """
    Get the raid performance for guild_id
    """
    query_str: str = (
        "SELECT "
        "p.player_id, p.nickname, rp.score AS score, "
        "rp.percent_of_average AS percent_of_average "
        "FROM players p "
        "LEFT JOIN raid_performance rp "
        "ON p.nickname = rp.nickname WHERE guild_id::text = %s;"
    )
    query_source: str = "raid_performance"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_member_points(guild_id: str, order_str: str) -> list:
    """
    Get the points a player has accumulated for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
        "SELECT "
        "* FROM member_points "
        "WHERE nickname IN "
        "(SELECT nickname FROM players WHERE guild_id = %s) "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "member_points"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def get_guild_from_nickname(nickname: str) -> str:
    """
    Get the guild_id for a known player nickname
    """
    query_str: str = (
        "SELECT guild_name "
        "FROM guild "
        "WHERE guild_id = "
        "(SELECT guild_id FROM players WHERE nickname = %s);"
    )
    query_source: str = "players"
    query_tuple: tuple = (nickname,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    if query_return:
        return query_return[0][0]
    else:
        return ""


def get_last_tb_data(guild_id: str) -> list:
    """
    Get the data on the last TB for guild_id, ordered nickname ASC
    """
    query_str: str = (
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
        "ORDER BY gm.nickname ASC;"
    )
    query_source: str = "latest TB"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def get_last_tb_data_ordered(guild_id: str, order_str: str) -> list | None:
    """
    Get the data on the last TB for guild_id, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    query_str: str = (
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
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = "latest TB"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return


def read_raid_progression(guild_id: str, timeframe: str, order_str: str) -> list:
    """
    Get the recent raid progression view for guild_id & timeframe, ordered by order_str
    """
    validated_order_str: str = get_valid_order_parameter(order_str)
    validated_timeframe: str = get_valid_timeframe_parameter(timeframe)
    query_str: str = (
        "SELECT "
        "nickname, last_raid_result, score_difference "
        f"FROM raid_progression_{validated_timeframe} "
        "WHERE nickname IN "
        "(SELECT nickname FROM players WHERE guild_id = %s) "
        f"ORDER BY {validated_order_str};"
    )
    query_source: str = f"raid_progression_{validated_timeframe}"
    query_tuple: tuple = (guild_id,)
    query_return: list = make_sql_query_single(query_str, query_source, query_tuple)
    return query_return
