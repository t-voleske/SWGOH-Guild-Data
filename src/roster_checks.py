"""
Check zeffo, mandalore and reva readiness of the rosters currently in the guild. 
Writes the results into the provided psql db.
"""

import os
import json
import logging
from dotenv import load_dotenv

from .read_data import read_players, read_roster_check, read_guild
from .update_data import updateRosterChecks
from .api_request import post_request
from .enter_data import enter_player_check
from .helper_functions import (
    check_none_str,check_none_list,is_list_or_tuple_instance,setup_logging
    )


logger = logging.getLogger("guild_data_app")
setup_logging()

def env_loading() -> tuple[str, str]:
    """
    Load the needed params from .env file
    """
    load_dotenv()
    # get guild and player interfaces for comlink
    guild_url_var: str = check_none_str(
        os.getenv("PASS"), "Error: Check .env file. PASS should not be None"
    )
    player_url_var: str = check_none_str(
        os.getenv("PLAYER_URL"), "Error: Check .env file. PLAYER_URL should not be None"
    )
    return (guild_url_var, player_url_var)


def check_roster(player_id: str, player_url: str) -> tuple:
    """
    Check the roster of a player for Zeffo, Mandalore & Reva readiness criteria
    Zeffo readiness: Cere R7 + Jedi Cal R7
    Mandalore: BKM R7 (as her unlock already implies the other requirements are ready)
    Reva: 5 Inquisitors, including at least two out of GI, Reva or Marrok
    """
    player = json.dumps(post_request(player_url, {"payload": {"playerId": player_id}}))
    player_data = json.loads(player).get("rosterUnit")
    player_name = json.loads(player).get("name")


    # Journey guide unit checks & default values
    reva_ready = False
    gi_r7 = any(
        t.get("definitionId") == "GRANDINQUISITOR:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    bkm_r7 = any(
        t.get("definitionId") == "MANDALORBOKATAN:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    reva_r7 = any(
        t.get("definitionId") == "THIRDSISTER:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    #-------
    # Check reva ready required units
    marrok_r7 = any(
        t.get("definitionId") == "MARROK:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    seventh_sister_r7 = any(
        t.get("definitionId") == "SEVENTHSISTER:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    fifth_brother_r7 = any(
        t.get("definitionId") == "FIFTHBROTHER:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    eighth_brother_r7 = any(
        t.get("definitionId") == "EIGHTHBROTHER:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    #ninth_sister_r7 =  any(
    #    t.get("definitionId") == "NINTHSISTER:SEVEN_STAR"
    #    and t.get("relic") is not None
    #    and t.get("relic").get("currentTier", 0) >= 9
    #    for t in player_data
    #)
    
    #Check, if at least a full team is ready for the reva mission
    all_inquisitors = [gi_r7, reva_r7, marrok_r7, seventh_sister_r7, fifth_brother_r7, eighth_brother_r7]
    key_units = [gi_r7, reva_r7, marrok_r7]

    if sum(all_inquisitors) >= 5 and sum(key_units) >= 2:
        reva_ready = True

    # Jedi Cal unlocked check
    jedi_cal_unlocked = any(
        t.get("definitionId") == "JEDIKNIGHTCAL:SEVEN_STAR" for t in player_data
    )
    # Check if Jedi Cal is at lvl 85
    jedi_cal_leveled = any(
        t.get("definitionId") == "JEDIKNIGHTCAL:SEVEN_STAR" and t.get("currentLevel") == 85
        for t in player_data
    )


    if not jedi_cal_leveled:
        check = reva_ready, gi_r7, bkm_r7, jedi_cal_unlocked, False, False, False, player_id
        logging.info("Jedi Cal not lvl 85 yet")
        logging.info(check)
        logging.info(player_name)
        return check

    
    # Relics checks
    jedi_cal_r7 = any(
        t.get("definitionId") == "JEDIKNIGHTCAL:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )
    cere_r7 = any(
        t.get("definitionId") == "CEREJUNDA:SEVEN_STAR"
        and t.get("relic") is not None
        and t.get("relic").get("currentTier", 0) >= 9
        for t in player_data
    )

    # Ability level checks
    skills = [
        t for t in player_data if t.get("definitionId") == "JEDIKNIGHTCAL:SEVEN_STAR"
        ][0]["skill"]
    jedi_cal_unique = any(
        t.get("id") == "uniqueskill_JEDIKNIGHTCAL01" and t.get("tier") >= 6 for t in skills
    )
    jedi_cal_leader = any(
        t.get("id") == "leaderskill_JEDIKNIGHTCAL" and t.get("tier") >= 5 for t in skills
    )

    jedi_cal_special_03 = any(
        t.get("id") == "specialskill_JEDIKNIGHTCAL03" and t.get("tier") >= 5 for t in skills
    )

    jedi_cal_special_02 = any(
        t.get("id") == "specialskill_JEDIKNIGHTCAL02" and t.get("tier") >= 6 for t in skills
    )

    jedi_cal_special_01 = any(
        t.get("id") == "specialskill_JEDIKNIGHTCAL01" and t.get("tier") >= 6 for t in skills
    )
    jedi_cal_skills_done = (
        jedi_cal_unique
        and jedi_cal_leader
        and jedi_cal_special_03
        and jedi_cal_special_02
        and jedi_cal_special_01
    )

    check = (
        reva_ready,
        gi_r7,
        bkm_r7,
        jedi_cal_unlocked,
        jedi_cal_r7,
        cere_r7,
        jedi_cal_skills_done,
        player_id,
    )
    logging.info("Else reached")
    logging.info(check)
    logging.info(player_name)
    return check

def run_roster_checks():
    """
    Run roster checks for all players in all guilds
    """
    env_vars = env_loading()
    guild_url_env = env_vars[0]
    player_url_env = env_vars[1]
    roster_check_data = check_none_list(
        read_roster_check(),
        "roster_check_data should not be None. Check read_roster_check function",
    )


    guilds_config = check_none_list(
        read_guild(), "read_guild should not be None! Check read_guild function"
    )
    logger.debug("Guilds config: %s", guilds_config)

    for g in guilds_config:
        read_players_data = check_none_list(
            read_players(g[0]),
            "read_players data should not be None. Check read_players function",
        )
        players = [
            check_none_list(is_list_or_tuple_instance(x), "Cannot be None")[0]
            if check_none_list(is_list_or_tuple_instance(x), "Cannot be None")[5] == g[0]
            else None
            for x in read_players_data
        ]
        logger.debug("players:")
        logger.debug(players)
        players = [x for x in players if x is not None]

        # Build set of player ids present in roster checks table for better lookup in next step
        present_player_ids = {value[0] for value in roster_check_data} 

        players_to_enter = [item for item in roster_check_data if item[0] not in present_player_ids]

        # Set of player ids for those, that need to be newly created in db
        players_to_enter_set = {value[0] for value in players_to_enter}

        # List of players that need to be updated in db
        players_to_update = [item for item in players if item[0] not in players_to_enter_set]
        logger.info("players_to_update: %s", players_to_update)

        # Iterate through all players that need an initial entry in the table
        roster_array = []
        for e in players_to_enter:
            roster_array.append(check_roster(e, player_url_env))

        enter_player_check(roster_array)

        # Iterate through all players that need an update in the table
        for d in players_to_update:
            updateRosterChecks(check_roster(d, player_url_env))

if __name__ == "__main__":
    run_roster_checks()
    logger.info("Roster checks complete")