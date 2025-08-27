from read_data import read_raid_performance_special
from enter_data import enter_log_raid_score




#----------------- Making a gp history log -----------------
db_scores = read_raid_performance_special()
#print(db_players)
raid_score_log = []
for e in db_scores: # type: ignore
    raid_score_log.append((e[0], e[2], e[3]))
print(raid_score_log)


### Needs a timer!
## Commented out to not spam the DB with data
enter_log_raid_score(raid_score_log)

#print(gp_logs)
