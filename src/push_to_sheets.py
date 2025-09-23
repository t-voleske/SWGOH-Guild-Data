import os
from pathlib import Path
import logging
import gspread
import pandas as pd
import psycopg2
from dotenv import load_dotenv
from .read_data import (
    read_players_data,
    read_tickets_weekly,
    read_tickets_monthly,
    read_member_points,
    read_guild,
    get_last_tb_data_ordered,
    read_raid_progression,
)
from .spreadsheet_operations import write_to_sheet, check_order, check_timeframe
from .helper_functions import check_none_str, check_none_list, setup_logging, floatify

logger = logging.getLogger("guild_data_app")
setup_logging()

load_dotenv()

if __name__ == "__main__":
    # Create gspread object to interact with spreadsheet API
    filepath: str = check_none_str(
        os.getenv("FILEPATH_CREDENTIALS"),
        "FILEPATH_CREDENTIALS should not be None. Check .env file",
    )
    gc = gspread.service_account(filename=Path(filepath))

    guilds_config = check_none_list(
        read_guild(), "guilds should not be None. Check read_guilds function"
    )
    logger.debug("After Import: %s", guilds_config)

    MAIN_SHEET = "Main"
    TICKETS_WEEKLY_SHEET = "Tickets_weekly"
    TICKETS_MONTHLY_SHEET = "Tickets_monthly"
    POINTS_WEEKLY_SHEET = "Points_weekly"
    LAST_TB_DATA_SHEET = "Last TB Data"
    RAID_PROGRESSION_SHEET = "Raid_progression"

    for g in guilds_config:
        try:
            df_main = pd.DataFrame(
                read_players_data(g[0], check_order(g, MAIN_SHEET)),
                columns=[
                    "nickname",
                    "last_activity",
                    "total_gp",
                    "raid_score",
                    "average_percent",
                    "zeffo_ready",
                    "tickets_lost_week",
                    "days_tickets_lost",
                ],
            )
            df_main = df_main.fillna("")
            df_main["total_gp"] = df_main["total_gp"].map(floatify)
            df_main["raid_score"] = df_main["raid_score"].map(floatify)
            df_main["average_percent"] = df_main["average_percent"].map(floatify)
        except psycopg2.DataError:
            logger.warning("%s does not have any player data to write to sheets.", g[1])

        write_to_sheet(g, "Main", df_main, "A2:H51")

        try:
            df_weekly = pd.DataFrame(
                read_tickets_weekly(g[0], check_order(g, TICKETS_WEEKLY_SHEET)),
                columns=["nickname", "tickets_lost", "days_tickets_lost", "full_days_lost"],
            )
            df_weekly = df_weekly.dropna()

            df_monthly = pd.DataFrame(
                read_tickets_monthly(g[0], check_order(g, TICKETS_MONTHLY_SHEET)),
                columns=["nickname", "tickets_lost", "days_tickets_lost", "full_days_lost"],
            )
            df_monthly = df_monthly.dropna()

            df_weekly_points = pd.DataFrame(
                read_member_points(g[0], check_order(g, POINTS_WEEKLY_SHEET)),
                columns=[
                    "player_id",
                    "nickname",
                    "last_activity_p",
                    "average_percent_p",
                    "zero_raid_score",
                    "zeffo_ready",
                    "tickets_weekly",
                    "total_points",
                ],
            )
            df_weekly_points = df_weekly_points.iloc[:, 1:]
        except psycopg2.DataError as e:
            logger.error(e)
            logger.warning(
                "%s does not have any weekly, monthly or points data to write to sheets.",
                g[1],
            )

        write_to_sheet(g, "Tickets_weekly", df_weekly, "A2:D51")
        write_to_sheet(g, "Tickets_monthly", df_monthly, "A2:D51")
        write_to_sheet(g, "Points_weekly", df_weekly_points, "A2:G51")

        try:
            df_tb = pd.DataFrame(
                get_last_tb_data_ordered(g[0], check_order(g, LAST_TB_DATA_SHEET)),
                columns=[
                    "nickname",
                    "total_territory_points",
                    "total_waves_completed",
                    "total_missions_attempted",
                    "wave_completion_ratio",
                    "phases_missed",
                    "created_at",
                ],
            )
            df_tb = df_tb.fillna("")
            df_tb["wave_completion_ratio"] = df_tb["wave_completion_ratio"].map(floatify)
            df_tb["created_at"] = pd.to_datetime(df_tb["created_at"], errors="coerce")
            df_tb["created_at"] = df_tb["created_at"].dt.strftime("%Y-%m-%dT%H:%M:%S")
        except psycopg2.DataError:
            logger.warning("%s does not have any TB data to write to sheets.", g[1])

        write_to_sheet(g, "Last TB Data", df_tb, "A2:G51")
        
        try:
            df_raid_progression = pd.DataFrame(
                read_raid_progression(g[0], check_timeframe(g, RAID_PROGRESSION_SHEET), check_order(g, RAID_PROGRESSION_SHEET)),
                columns=[
                    "nickname",
                    "last_raid_result",
                    "score_difference",
                ],
            )
            df_raid_progression = df_raid_progression.fillna("")
            df_raid_progression["last_raid_result"] = df_raid_progression["last_raid_result"].map(floatify)
            df_raid_progression["score_difference"] = df_raid_progression["score_difference"].map(floatify)
        except psycopg2.DataError:
            logger.warning("%s does not have any raid_progression data to write to sheets.", g[1])


        write_to_sheet(g, "Raid_progression", df_raid_progression, "A2:C51")
