import json
import os
from dotenv import load_dotenv
from read_data import read_guild, read_players
from update_data import updateLastRaidResult
from api_request import post_request
from helper_functions import check_none

load_dotenv()
guild_url : str = check_none(os.getenv("GUILD_URL"), 'Error: Check .env file. GUILD_URL should not be None')

guilds_config = check_none(read_guild(), 'guilds should not be None. Check read_guilds function')
#print('After Import:')
#print(guilds_config)

for g in guilds_config:
    #print('g:')
    #print(g)
    guild = json.dumps(post_request(guild_url, {"payload": {"guildId": g[0], "includeRecentGuildActivityInfo": True}}))
    raid_results = list(filter(lambda t: t['raidId'] == "order66", json.loads(guild)['guild']['recentRaidResult']))[0]['raidMember']
    #print(raid_results)

    #print("read_players(g[0])")
    #print(read_players(g[0]))
    players = check_none(read_players(g[0]), 'players should not be None. Check read_players function')
    for e in players:
        print(e[0])
        pre_result = list(filter(lambda t: t['playerId'] == e[0], raid_results))
        if pre_result.__len__() > 0:
            raid_result = pre_result[0]['memberProgress']
        else:
            raid_result = None

        updateLastRaidResult(raid_result, e[0])

