import json
import os
import logging
from dotenv import load_dotenv
from read_data import read_guild, read_players
from update_data import updateLastRaidResult
from api_request import post_request
from helper_functions import check_none_str, check_none_list, setup_logging


logger = logging.getLogger("guild_data_app")
setup_logging()

if __name__ == "__main__":
    load_dotenv()
    guild_url: str = check_none_str(
        os.getenv("GUILD_URL"), "Error: Check .env file. GUILD_URL should not be None"
    )

    guilds_config = check_none_list(
        read_guild(), "guilds should not be None. Check read_guilds function"
    )
    logger.debug("Guilds_config: %s", guilds_config)


    for g in guilds_config:
        logger.debug("g: %s", g)
        guild = json.dumps(
            post_request(
                guild_url,
                {"payload": {"guildId": g[0], "includeRecentGuildActivityInfo": True}},
            )
        )
        raid_results = list(
            filter(
                lambda t: t["raidId"] == "order66",
                json.loads(guild)["guild"]["recentRaidResult"],
            )
        )[0]["raidMember"]
        logger.debug("raid_results: %s", raid_results)

        logger.info("read_players(g[0]): %s", read_players(g[0]))
        players = check_none_list(
            read_players(g[0]), "players should not be None. Check read_players function"
        )
        for e in players:
            logger.info("e[0]: %s", e[0])
            pre_result = [t for t in raid_results if t["playerId"] == e[0]]
            if pre_result:
                RAID_RESULT = pre_result[0]["memberProgress"]
            else:
                RAID_RESULT = None

            updateLastRaidResult(RAID_RESULT, e[0])
