import json
import os
from datetime import datetime as dt
import logging
from dotenv import load_dotenv

from api_request import post_request
from archive_players import archive_process
from enter_data import enter_players
from read_data import read_guild, read_players
from update_data import remove_from_guild, update_activity, updateGP
from helper_functions import check_none_str, check_none_list, setup_logging


logger = logging.getLogger("guild_data_app")
setup_logging()

dtime = dt.now()


class Player:
    def __init__(
        self,
        player_id: str,
        nickname: str,
        galactic_power: int,
        fleet_gp: int,
        ground_gp: int,
        guild_id: str,
        last_activity_time,
        current_tickets: int,
    ):
        self.player_id = player_id
        self.nickname = nickname
        self.guild_id = guild_id
        self.galactic_power = galactic_power
        self.fleet_gp = fleet_gp
        self.ground_gp = ground_gp
        self.last_activity_time = dt.fromtimestamp(int(last_activity_time) / 1000)
        self.current_tickets = current_tickets
        logger.debug(self.nickname)
        logger.debug(self.last_activity_time)
        update_activity(self.last_activity_time, self.player_id)
        updateGP(self.galactic_power, self.player_id)

    def __str__(self):
        return f"{self.nickname}"

    def dbify(self):
        return (
            self.player_id,
            self.nickname,
            self.galactic_power,
            self.guild_id,
            self.last_activity_time,
        )

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    guild_url: str = check_none_str(
        os.getenv("GUILD_URL"), "Error: Check .env file. GUILD_URL should not be None"
    )

    guilds_config = check_none_list(
        read_guild(), "guilds should not be None. Check read_guilds function"
    )
    logger.debug("After Import: %s", guilds_config)


    for g in guilds_config:
        guild = json.dumps(
            post_request(
                guild_url,
                {"payload": {"guildId": g[0], "includeRecentGuildActivityInfo": True}},
            )
        )
        data = json.loads(guild)["guild"]["member"]
        logger.debug("guild: %s", guild)
        playerArr = []
        nicknameArr = []
        for m in data:
            playerArr.append(
                Player(
                    m["playerId"],
                    m["playerName"],
                    m["galacticPower"],
                    m["shipGalacticPower"],
                    m["characterGalacticPower"],
                    g[0],
                    m["lastActivityTime"],
                    600
                    - int(
                        list(filter(lambda t: t["type"] == 2, m["memberContribution"]))[0][
                            "currentValue"
                        ]
                    ),
                )
            )
            nicknameArr.append(m["playerName"])

        db_nicknames = []
        db_players = check_none_list(
            read_players(g[0]), "Players should not be None. Check read_players function"
        )
        for n in db_players:
            db_nicknames.append(n[1])

        to_add = list(set(nicknameArr) - set(db_nicknames))
        to_remove = list(set(db_nicknames) - set(nicknameArr))

        players_to_add = [x for x in playerArr if x.nickname in to_add]
        players_to_remove = [y for y in to_remove if y[1] not in playerArr]
        enterArr = []
        for w in players_to_add:
            enterArr.append(w.dbify())

        enter_players(enterArr)

        logger.info("--players to remove--")
        logger.info(players_to_remove)
        for i in players_to_remove:
            remove_from_guild(i)

    # archive players after their guild affiliation was removed
    archive_process()
