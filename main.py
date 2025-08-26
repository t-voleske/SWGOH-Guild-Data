import os
import psycopg2
import json
from dotenv import load_dotenv
from read_data import read_guild, read_players
from api_request import post_request
from enter_data import enter_players, log_gp
from update_data import remove_son, updateActivity, updateGP
from datetime import datetime as dt

dtime = dt.now()

class Player:
    def __init__(self, player_id, nickname, galactic_power, fleet_gp, ground_gp, guild_id, last_activity_time, current_tickets):
        self.player_id = player_id
        self.nickname = nickname
        self.guild_id = guild_id
        self.galactic_power = galactic_power
        self.fleet_gp = fleet_gp
        self.ground_gp = ground_gp
        self.last_activity_time = dt.fromtimestamp(int(last_activity_time)/1000)
        self.current_tickets = current_tickets
        print(self.nickname)
        print(self.last_activity_time)
        updateActivity(self.last_activity_time, self.player_id)
        updateGP(self.galactic_power, self.player_id)
    
    def __str__(self):
        return f"{self.nickname}"
    
    def returnNickname(self):
        return self.nickname
    
    def dbify(self):
        return (self.player_id, self.nickname, self.galactic_power, self.guild_id, self.last_activity_time) 

# Load environment variables from .env file
load_dotenv()
guild_url = os.getenv("GUILD_URL")
son_guild_id = read_guild()

guild = json.dumps(post_request(guild_url, {"payload": {"guildId": son_guild_id, "includeRecentGuildActivityInfo": True}}))
data = json.loads(guild)['guild']['member']
#print(guild)
playerArr = []
nicknameArr = []
for m in data:
    #print(list(filter(lambda t: t['type'] == 2, m['memberContribution']))[0]['currentValue'])
    playerArr.append(Player(m['playerId'], m['playerName'], m['galacticPower'], m['shipGalacticPower'], m['characterGalacticPower'], son_guild_id, m['lastActivityTime'], 600 - int(list(filter(lambda t: t['type'] == 2, m['memberContribution']))[0]['currentValue'])))
    nicknameArr.append(m['playerName'])


db_nicknames = []
db_players = read_players()
for n in db_players: # type: ignore
    db_nicknames.append(n[1])    

to_add = list(set(nicknameArr) - set(db_nicknames))
to_remove = list(set(db_nicknames) - set(nicknameArr))
print(to_add)

players_to_add = list(filter(lambda x: x.nickname in to_add, playerArr))
players_to_remove = list(filter(lambda y: y[1] not in playerArr, to_remove)) # type: ignore

enterArr = []
for w in players_to_add:
    enterArr.append(w.dbify())

enter_players(enterArr)

print("--players to remove--")
print(players_to_remove)
for i in players_to_remove:
    remove_son(i)
 


#----------------- Making a gp history log -----------------
db_players = read_players()
#print(db_players)
gp_logs = []
for e in db_players: # type: ignore
    gp_logs.append((e[0], e[2], dtime))


### Needs a timer!
## Commented out to not spam the DB with data
#log_gp(gp_logs)


##Maybe player level api requests
#player_api_arr = []
#for a in db_players: # type: ignore
#    player_api_arr.append(json.dumps(post_request(guild_url, {"payload": {"playerId": a[0]}})))

#print(player_api_arr)[0] # type: ignore
