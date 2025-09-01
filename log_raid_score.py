from read_data import read_raid_performance_by_guild, read_guild
from enter_data import enter_raid_score_log

raid_score_log = []
guilds_config = read_guild()
#print('After Import:')
#print(guilds_config)
if guilds_config is None:
    raise ValueError('guilds should not be None. Check read_guilds function')

for g in guilds_config:
    db_scores = read_raid_performance_by_guild(g[0])
    if db_scores is None:
        raise ValueError('Raid performance did not read correctly. Check read_raid_performance_special function')
    #print(db_players)
    for e in db_scores:
        raid_score_log.append((e[0], e[2], e[3]))
    print(raid_score_log)

enter_raid_score_log(raid_score_log)

