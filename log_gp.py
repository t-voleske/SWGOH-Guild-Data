from read_data import read_players, read_guild
from enter_data import enter_gp_logs
from helper_functions import check_none

gp_logs = []
guilds_config = check_none(read_guild(), 'Guild should not be None. Check read_guild function')
#print('After Import:')
#print(guilds_config)

for g in guilds_config:
    #print('g:')
    #print(g)
    db_players = check_none(read_players(g[0]), 'Players should not be None. Check read_players function')

    for e in db_players:
        gp_logs.append((e[0], e[2]))

enter_gp_logs(gp_logs)
