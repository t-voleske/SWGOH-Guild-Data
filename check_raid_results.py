import os
import json
from dotenv import load_dotenv
from read_data import read_guild, read_players
from update_data import updateLastRaidResult
from api_request import post_request

load_dotenv()
guild_url = os.getenv("GUILD_URL")
son_guild_id = read_guild()

guild = json.dumps(post_request(guild_url, {"payload": {"guildId": son_guild_id, "includeRecentGuildActivityInfo": True}}))
raid_results = list(filter(lambda t: t['raidId'] == "order66", json.loads(guild)['guild']['recentRaidResult']))[0]['raidMember']
print(raid_results)

players = read_players()
if players is None:
    raise ValueError('players should not be None. Check read_players function')
for e in players:
    print(e[0])
    pre_result = list(filter(lambda t: t['playerId'] == e[0], raid_results))
    if pre_result.__len__() > 0:
        raid_result = pre_result[0]['memberProgress']
    else:
        raid_result = None

    updateLastRaidResult(raid_result, e[0])

