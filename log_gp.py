from read_data import read_players, read_guild
from enter_data import enter_gp_logs

gp_logs = []
guilds_config = read_guild()
#print('After Import:')
#print(guilds_config)
if guilds_config is None:
    raise ValueError('guilds should not be None. Check read_guilds function')

for g in guilds_config:
    #print('g:')
    #print(g)
    db_players = read_players(g[0])
    if db_players is None:
        raise ValueError('Players did not read correctly. Check read_players function')

    for e in db_players:
        gp_logs.append((e[0], e[2]))

enter_gp_logs(gp_logs)
