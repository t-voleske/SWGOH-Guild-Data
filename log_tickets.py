import os
import json
from dotenv import load_dotenv
from read_data import read_guild
from api_request import post_request
from enter_data import enter_tickets
from datetime import datetime as dt

dtime = dt.now()
dtime = dtime.strftime('%Y-%m-%d %H:%M:%S')


# Load environment variables from .env file
load_dotenv()
guild_url = os.getenv("GUILD_URL")
son_guild_id = read_guild()

#Request current guild data from comlink API
guild = json.dumps(post_request(guild_url, {"payload": {"guildId": son_guild_id, "includeRecentGuildActivityInfo": True}}))
data = json.loads(guild)['guild']['member']
#print(guild)

#Make list of all players' tickets for the day
tickets = []
for m in data:
    tickets.append((m['playerId'], dtime, 600 - int(list(filter(lambda t: t['type'] == 2, m['memberContribution']))[0]['currentValue'])))

#filter out players that reached the required 600 tickets
tickets = list(filter(lambda x: x[2] > 0, tickets))
enter_tickets(tickets)

#is Current