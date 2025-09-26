import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from .read_data import read_guild
from .api_request import post_request
from .enter_data import enter_tickets
from .helper_functions import check_none_list, check_none_str, setup_logging


logger = logging.getLogger("guild_data_app")
setup_logging()


# guarding against data entry out of reset window
#def is_around_reset_time(reset_time, now=None):
#    if now is None:
#        now = datetime.now()
#    current_time = now.time()
#    time_in_2_minutes = (now + timedelta(minutes=2)).time()
#    if time_in_2_minutes > current_time:
#        return current_time < reset_time <= time_in_2_minutes
#    return (reset_time > current_time) or (reset_time <= time_in_2_minutes)

def is_around_reset_time(reset_time, now=None):
    if now is None:
        now = datetime.now()
    
    reset_datetime = now.replace(
        hour=reset_time.hour, minute=reset_time.minute, second=reset_time.second
    )

    if reset_datetime < now:
        reset_datetime += timedelta(days=1)
        
    window_start = reset_datetime - timedelta(minutes=2)
    
    return window_start <= now <= reset_datetime


def process_ticket_log():
    """
    Checks if it's a guild's reset time, if so, fetches guild data and logs tickets to DB.
    """
    load_dotenv()
    guild_url = check_none_str(
        os.getenv("GUILD_URL"), "Error: Check .env file. GUILD_URL should not be None"
    )  # url for comlink/guild interface

    guilds_config = check_none_list(
        read_guild(), "guilds should not be None. Check read_guilds function"
    )

    for g in guilds_config:
        if not is_around_reset_time(g[2]):
            logger.debug("Continue triggered. Not reset time")
            continue
        guild = json.dumps(
            post_request(
                guild_url,
                {"payload": {"guildId": g[0], "includeRecentGuildActivityInfo": True}},
            )
        )
        data = json.loads(guild)["guild"]["member"]

        tickets = [
            (
                m["playerId"],
                600
                - int(
                    list(filter(lambda t: t["type"] == 2, m["memberContribution"]))[0][
                        "currentValue"
                    ]
                ),
            )
            for m in data
        ]

        # filter out players that reached the required 600 tickets
        tickets = list(filter(lambda x: x[1] > 0, tickets))
        if tickets:
            logger.info("Logging tickets for: %s", g[1])
            enter_tickets(tickets)
        else:
            logger.info("No tickets to log for: %s", g[1])

if __name__ == "__main__":
    process_ticket_log()
