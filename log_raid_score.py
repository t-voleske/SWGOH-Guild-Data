from read_data import read_raid_performance_by_guild, read_guild
from enter_data import enter_raid_score_log
from helper_functions import check_none

raid_score_log = []
guilds_config = check_none(read_guild(), 'Guild should not be None. Check read_players function')
#print('After Import:')
#print(guilds_config)

for g in guilds_config:
    db_scores = check_none(read_raid_performance_by_guild(g[0]), 'Value should not be None. Check read_raid_performance_by_guild function')
    #print(db_players)
    for e in db_scores:
        raid_score_log.append((e[0], e[2], e[3]))
    print(raid_score_log)

enter_raid_score_log(raid_score_log)

