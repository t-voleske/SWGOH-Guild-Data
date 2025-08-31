from read_data import read_raid_performance_special
from enter_data import enter_log_raid_score


db_scores = read_raid_performance_special()
if db_scores is None:
    raise ValueError('Raid performance did not read correctly. Check read_raid_performance_special function')
#print(db_players)
raid_score_log = []
for e in db_scores:
    raid_score_log.append((e[0], e[2], e[3]))
print(raid_score_log)

enter_log_raid_score(raid_score_log)

