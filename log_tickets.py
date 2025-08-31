import os
import json
from dotenv import load_dotenv
from read_data import read_guild
from api_request import post_request
from enter_data import enter_tickets

load_dotenv()
guild_url = os.getenv("GUILD_URL") #url for comlink/guild interface
# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds
# --------------------------------------------------------------------------------------------
guild_id = read_guild()

guild = json.dumps(post_request(guild_url, {"payload": {"guildId": guild_id, "includeRecentGuildActivityInfo": True}}))
data = json.loads(guild)['guild']['member']

#Make list of all players' tickets for the day
tickets = []
for m in data:
    tickets.append((m['playerId'], 600 - int(list(filter(lambda t: t['type'] == 2, m['memberContribution']))[0]['currentValue'])))

#filter out players that reached the required 600 tickets
tickets = list(filter(lambda x: x[1] > 0, tickets))
enter_tickets(tickets)

#is Current