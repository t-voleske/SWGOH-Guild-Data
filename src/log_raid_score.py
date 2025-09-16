from src.read_data import read_raid_performance_by_guild, read_guild
from src.enter_data import enter_raid_score_log
from src.helper_functions import check_none_list, setup_logging
import logging

logger = logging.getLogger("guild_data_app")
setup_logging()

raid_score_log = []
guilds_config = check_none_list(
    read_guild(), "Guild should not be None. Check read_players function"
)
logger.debug("After Import: %s", guilds_config)

for g in guilds_config:
    logger.debug("g[0]: %s", g[0])
    db_scores = check_none_list(
        read_raid_performance_by_guild(g[0]),
        "Value should not be None. Check read_raid_performance_by_guild function",
    )
    logger.debug("db_scores: %s", db_scores)
    for e in db_scores:
        raid_score_log.append((e[0], e[2], e[3]))
    logger.debug("raid_score_log: %s", raid_score_log)
    logger.info("Logging raid performance for: %s", g[1])

enter_raid_score_log(raid_score_log)
