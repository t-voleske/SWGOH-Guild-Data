from read_data import read_players_raw, read_guild
from enter_data import enter_player_archive
from remove_data import remove_from_players
from helper_functions import check_none_list, setup_logging
import logging

logger = logging.getLogger("guild_data_app")


def archive_process():
    setup_logging()
    guilds_config = check_none_list(
        read_guild(), "Error: read_guild function should not return None"
    )

    raw_players_data = check_none_list(
        read_players_raw(), "Error: read_players_raw function should not return None"
    )

    guild_ids = [g[0] for g in guilds_config]
    logger.info("guild ids: %s", guild_ids)
    filtered_players_data = [
        (x[0], x[1], x[2], x[5]) for x in raw_players_data if x[5] not in guild_ids
    ]
    logger.debug(filtered_players_data)

    enter_player_archive(filtered_players_data)
    to_remove = [(i[0],) for i in filtered_players_data]
    logger.debug("to remove:")
    logger.debug(to_remove)
    remove_from_players(to_remove)
