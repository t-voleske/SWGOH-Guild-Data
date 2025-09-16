from src.read_data import read_players, read_guild
from src.enter_data import enter_gp_logs
from src.helper_functions import check_none_list, setup_logging
import logging

logger = logging.getLogger("guild_data_app")
setup_logging()


gp_logs = []
guilds_config = check_none_list(
    read_guild(), "Guild should not be None. Check read_guild function"
)
logger.debug("After Import: %s", guilds_config)

for g in guilds_config:
    logger.debug("g: %s", g)

    db_players = check_none_list(
        read_players(g[0]), "Players should not be None. Check read_players function"
    )

    for e in db_players:
        gp_logs.append((e[0], e[2]))
    logger.info("Logging GP for: %s", g[1])

enter_gp_logs(gp_logs)
