from read_data import read_players
from enter_data import enter_gp_logs



db_players = read_players()
if db_players is None:
    raise ValueError('Players did not read correctly. Check read_players function')
gp_logs = []
for e in db_players:
    gp_logs.append((e[0], e[2]))

enter_gp_logs(gp_logs)
