from read_data import read_players_raw, read_guild
from enter_data import enter_player_archive
from remove_data import remove_from_players

def archive_process():
    guilds_config = read_guild()

    if guilds_config is None:
        raise ValueError('guilds should not be None. Check read_guilds function')

    raw_players_data = read_players_raw()
    if raw_players_data is None:
        raise ValueError('Players did not read correctly. Check read_players_raw function')
    guild_ids = [g[0] for g in guilds_config]
    #print(guild_ids)
    filtered_players_data = [(x[0], x[1], x[2], x[5]) for x in raw_players_data if x[5] not in guild_ids]
    #print(filtered_players_data)

    enter_player_archive(filtered_players_data)
    to_remove = [(i[0], ) for i in filtered_players_data]
    #print(to_remove)
    remove_from_players(to_remove)
