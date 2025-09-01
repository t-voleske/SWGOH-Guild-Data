import os
import json
from dotenv import load_dotenv
from read_data import read_guild
from api_request import post_request
from enter_data import enter_tickets
from datetime import datetime, timedelta

#guarding against data entry out of reset window
def is_around_reset_time(reset_time):
    now = datetime.now()
    current_time = now.time()
    time_in_2_minutes = (now + timedelta(minutes=2)).time()
    if time_in_2_minutes > current_time:
        return current_time < reset_time <= time_in_2_minutes
    return (reset_time > current_time) or (reset_time <= time_in_2_minutes)

load_dotenv()
guild_url = os.getenv("GUILD_URL") #url for comlink/guild interface

guilds_config = read_guild()
if guilds_config is None:
    raise ValueError('guilds should not be None. Check read_guilds function')

for g in guilds_config:
    if not is_around_reset_time(g[2]):
        print('Continue triggered. Not reset time')
        continue
    guild = json.dumps(post_request(guild_url, {"payload": {"guildId": g[0], "includeRecentGuildActivityInfo": True}}))
    data = json.loads(guild)['guild']['member']

    tickets = [(m['playerId'], 600 - int(list(filter(lambda t: t['type'] == 2, m['memberContribution']))[0]['currentValue'])) for m in data]

    #filter out players that reached the required 600 tickets
    tickets = list(filter(lambda x: x[1] > 0, tickets))
    enter_tickets(tickets)