import os
import psycopg2
import json
from dotenv import load_dotenv
from read_data import read_guild, read_players, read_roster_check
from update_data import updateRosterChecks
from api_request import post_request
from enter_data import enter_player_check

# Load environment variables from .env file
load_dotenv()
guild_url = os.getenv("GUILD_URL")
player_url = os.getenv("PLAYER_URL")
son_guild_id = read_guild()

def check_roster(p):
    print(p)
    player = json.dumps(post_request(player_url, {"payload": {"playerId": p}}))
    player_data = json.loads(player)['rosterUnit']

    #7 star checks
    cal_7_star = list(filter(lambda t: t['definitionId'] == 'CALKESTIS:SEVEN_STAR', player_data)).__len__() > 0
    cere_7_star = list(filter(lambda t: t['definitionId'] == 'CEREJUNDA:SEVEN_STAR', player_data)).__len__() > 0
    merrin_7_star = list(filter(lambda t: t['definitionId'] == 'MERRIN:SEVEN_STAR', player_data)).__len__() > 0
    tarfful_7_star = list(filter(lambda t: t['definitionId'] == 'TARFFUL:SEVEN_STAR', player_data)).__len__() > 0
    saw_7_star = list(filter(lambda t: t['definitionId'] == 'SAWGERRERA:SEVEN_STAR', player_data)).__len__() > 0
    all_7_star = (cal_7_star and cere_7_star and merrin_7_star and tarfful_7_star and saw_7_star)

    #Jedi Cal unlocked check
    jedi_cal_unlocked = list(filter(lambda t: t['definitionId'] == 'JEDIKNIGHTCAL:SEVEN_STAR', player_data)).__len__() > 0

    #Check if Jedi Cal is at lvl 85
    jedi_cal_leveled = list(filter(lambda t: (t['definitionId'] == 'JEDIKNIGHTCAL:SEVEN_STAR' and t['currentLevel'] == 85), player_data)).__len__() > 0
    if not jedi_cal_leveled:
        print("A")
        check = all_7_star, jedi_cal_unlocked, False, False, False, p
        print(check)
        return check

    else:
        print("B")
        #Relics checks
        jedi_cal_r7 = list(filter(lambda t: t['definitionId'] == 'JEDIKNIGHTCAL:SEVEN_STAR' and t['relic']['currentTier'] >= 9, player_data)).__len__() > 0
        cere_r7 = list(filter(lambda t: t['definitionId'] == 'CEREJUNDA:SEVEN_STAR' and t['relic']['currentTier'] >= 9, player_data)).__len__() > 0
        both_r7 = jedi_cal_r7 and cere_r7

        #Omi & Zeta check
        skills = list(filter(lambda t: t['definitionId'] == 'JEDIKNIGHTCAL:SEVEN_STAR', player_data))[0]['skill']
        jedi_cal_unique = list(filter(lambda t: (t['id'] == 'uniqueskill_JEDIKNIGHTCAL01' and t['tier'] >= 6), skills)).__len__() > 0
        jedi_cal_leader = list(filter(lambda t: (t['id'] == 'leaderskill_JEDIKNIGHTCAL' and t['tier'] >= 5), skills)).__len__() > 0
        jedi_cal_special_03 = list(filter(lambda t: (t['id'] == 'specialskill_JEDIKNIGHTCAL03' and t['tier'] >= 5), skills)).__len__() > 0
        jedi_cal_special_02 = list(filter(lambda t: (t['id']== 'specialskill_JEDIKNIGHTCAL02' and t['tier'] >= 6), skills)).__len__() > 0
        jedi_cal_special_01 = list(filter(lambda t: (t['id'] == 'specialskill_JEDIKNIGHTCAL01' and t['tier'] >= 6), skills)).__len__() > 0
        jedi_cal_skills_done = jedi_cal_unique and jedi_cal_leader and jedi_cal_special_03 and jedi_cal_special_02 and jedi_cal_special_01

        check = all_7_star, jedi_cal_unlocked, jedi_cal_r7, cere_r7, jedi_cal_skills_done, p
        print(check)
        return check

#Get current data from player_roster_checks table
roster_check_data = read_roster_check()
#List of guild member player_ids
players = list(map(lambda x: x[0] if x[3] == 'Xyw6K1R1SOazMbS94TX7fw' else None, read_players())) # type: ignore
players = [x for x in players if x is not None]

#filter for players that are zeffo_ready == True, then map entry to their player_id
alrady_zeffo_ready = list(map(lambda y: y[0], list(filter(lambda x: x[5] == True, roster_check_data)))) # type: ignore
print(alrady_zeffo_ready)
#filter for players that are zeffo_ready == False, then map entry to their player_id
players_to_update = list(map(lambda y: y[0], list(filter(lambda x: x[5] == False, roster_check_data)))) # type: ignore
print(players_to_update)

#Remove zeffo ready and players to update from players list
players = list(filter(lambda x: x not in alrady_zeffo_ready and x not in players_to_update, players))


#Iterate through all players that need an initial entry in the table
roster_array = []
for e in players: # type: ignore
    roster_array.append(check_roster(e))
enter_player_check(roster_array)

#Iterate through all players that need an update in the table
for d in players_to_update: # type: ignore
    updateRosterChecks(check_roster(d))


#enter_player_check(player_checks)
#print("Roster check result:")
#print(read_roster_check())


