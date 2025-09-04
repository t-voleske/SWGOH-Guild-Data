import os
import json
import logging
from dotenv import load_dotenv
from read_data import read_players, read_roster_check, read_guild
from update_data import updateRosterChecks
from api_request import post_request
from enter_data import enter_player_check
from helper_functions import check_none, is_list_or_tuple_instance, setup_logging

logger = logging.getLogger("guild_data_app")
setup_logging()


load_dotenv()
# get guild and player interfaces for comlink
guild_url: str = check_none(
    os.getenv("PASS"), "Error: Check .env file. GUILD_URL should not be None"
)
player_url: str = check_none(
    os.getenv("PLAYER_URL"), "Error: Check .env file. GUILD_URL should not be None"
)


def check_roster(p):
    player = json.dumps(post_request(player_url, {"payload": {"playerId": p}}))
    player_data = json.loads(player)["rosterUnit"]

    # 7 star checks
    cal_7_star = any(t["definitionId"] == "CALKESTIS:SEVEN_STAR" for t in player_data)
    cere_7_star = any(t["definitionId"] == "CEREJUNDA:SEVEN_STAR" for t in player_data)
    merrin_7_star = any(t["definitionId"] == "MERRIN:SEVEN_STAR" for t in player_data)
    tarfful_7_star = any(t["definitionId"] == "TARFFUL:SEVEN_STAR" for t in player_data)
    saw_7_star = any(t["definitionId"] == "SAWGERRERA:SEVEN_STAR" for t in player_data)
    all_7_star = all(
        [cal_7_star, cere_7_star, merrin_7_star, tarfful_7_star, saw_7_star]
    )

    # Jedi Cal unlocked check
    jedi_cal_unlocked = any(
        t["definitionId"] == "JEDIKNIGHTCAL:SEVEN_STAR" for t in player_data
    )
    # Check if Jedi Cal is at lvl 85
    jedi_cal_leveled = any(
        t["definitionId"] == "JEDIKNIGHTCAL:SEVEN_STAR" and t["currentLevel"] == 85
        for t in player_data
    )
    if not jedi_cal_leveled:
        check = all_7_star, jedi_cal_unlocked, False, False, False, p
        logging.info("Jedi Cal not lvl 85 yet")
        return check

    else:
        # Relics checks
        jedi_cal_r7 = any(
            t["definitionId"] == "JEDIKNIGHTCAL:SEVEN_STAR"
            and t["relic"]["currentTier"] >= 9
            for t in player_data
        )
        cere_r7 = any(
            t["definitionId"] == "CEREJUNDA:SEVEN_STAR"
            and t["relic"]["currentTier"] >= 9
            for t in player_data
        )

        # Ability level checks
        skills = [
            t for t in player_data if t["definitionId"] == "JEDIKNIGHTCAL:SEVEN_STAR"
        ][0]["skill"]
        jedi_cal_unique = any(
            t["id"] == "uniqueskill_JEDIKNIGHTCAL01" and t["tier"] >= 6 for t in skills
        )
        jedi_cal_leader = any(
            t["id"] == "leaderskill_JEDIKNIGHTCAL" and t["tier"] >= 5 for t in skills
        )

        jedi_cal_special_03 = any(
            t["id"] == "specialskill_JEDIKNIGHTCAL03" and t["tier"] >= 5 for t in skills
        )

        jedi_cal_special_02 = any(
            t["id"] == "specialskill_JEDIKNIGHTCAL02" and t["tier"] >= 6 for t in skills
        )

        jedi_cal_special_01 = any(
            t["id"] == "specialskill_JEDIKNIGHTCAL01" and t["tier"] >= 6 for t in skills
        )
        jedi_cal_skills_done = (
            jedi_cal_unique
            and jedi_cal_leader
            and jedi_cal_special_03
            and jedi_cal_special_02
            and jedi_cal_special_01
        )

        check = (
            all_7_star,
            jedi_cal_unlocked,
            jedi_cal_r7,
            cere_r7,
            jedi_cal_skills_done,
            p,
        )
        logging.info("Else reached")
        logging.info(check)
        return check


roster_check_data = check_none(
    read_roster_check(),
    "roster_check_data should not be None. Check read_roster_check function",
)


guilds_config = check_none(
    read_guild(), "read_guild should not be None! Check read_guild function"
)
logger.debug("Guilds config: %s", guilds_config)

for g in guilds_config:
    read_players_data = check_none(
        read_players(g[0]),
        "read_players data should not be None. Check read_players function",
    )

    players = [
        check_none(is_list_or_tuple_instance(x), "Cannot be None")[0]
        if check_none(is_list_or_tuple_instance(x), "Cannot be None")[5] == g[0]
        else None
        for x in read_players_data
    ]
    logger.info("players:")
    logger.info(players)
    players = [x for x in players if x is not None]

    # No update needed for players already zeffo_ready == True
    already_zeffo_ready = [
        y[0]
        for y in roster_check_data
        if check_none(is_list_or_tuple_instance(y), "Canno be None")[6]
    ]
    # filter for players that are zeffo_ready == False, then map entry to their player_id
    players_to_update = [
        y[0]
        for y in roster_check_data
        if check_none(is_list_or_tuple_instance(y), "Canno be None")[6] is False
    ]
    logger.info("players_to_update: %s", players_to_update)

    # Remove zeffo ready and players to update from players list
    players = [
        x
        for x in players
        if x not in already_zeffo_ready and x not in players_to_update
    ]

    # Iterate through all players that need an initial entry in the table
    roster_array = []
    for e in players:
        roster_array.append(check_roster(e))

    enter_player_check(roster_array)

    # Iterate through all players that need an update in the table
    for d in players_to_update:
        updateRosterChecks(check_roster(d))
