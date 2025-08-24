from read_data import read_players
from enter_data import log_gp
from datetime import datetime as dt

dtime = dt.now()


#----------------- Making a gp history log -----------------
db_players = read_players()
#print(db_players)
gp_logs = []
for e in db_players: # type: ignore
    gp_logs.append((e[0], e[2], dtime))


### Needs a timer!
## Commented out to not spam the DB with data
log_gp(gp_logs)
