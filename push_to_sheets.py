import os
from pathlib import Path
import gspread
import pandas as pd
from dotenv import load_dotenv
from helper_functions import check_none
from read_data import (
    read_players_data,
    read_tickets_weekly,
    read_tickets_monthly,
    read_member_points,
    read_guild,
)

load_dotenv()


def floatify(x):
    if x == "":
        return "-"
    return float(x)


# --------------------------------------------------------------------------------------------
# TO DO: Add support for multiple guilds (spreadsheet needs to be set up separately)
# --------------------------------------------------------------------------------------------
# Create gspread object to interact with spreadsheet API
filepath: str = check_none(
    os.getenv("FILEPATH_CREDENTIALS"),
    "FILEPATH_CREDENTIALS should not be None. Check .env file",
)
gc = gspread.service_account(filename=Path(filepath))

guilds_config = read_guild()
# print('After Import:')
# print(guilds_config)
if guilds_config is None:
    raise ValueError("guilds should not be None. Check read_guilds function")

for g in guilds_config:
    # open spreadsheet in gspread & create gspread objects for each worksheet
    print(g)
    sh = gc.open(g[3])
    main = sh.worksheet("Main")
    weekly = sh.worksheet("Tickets_weekly")
    monthly = sh.worksheet("Tickets_monthly")
    points_weekly = sh.worksheet("Points_weekly")

    # Prepare data for Main sheet
    df = pd.DataFrame(
        read_players_data(g[0]),
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
    df = df.fillna("")
    df["average_percent"] = df["average_percent"].map(floatify)
    df["total_gp"] = df["total_gp"].map(floatify)
    df["raid_score"] = df["raid_score"].map(floatify)
    # print(df)

    # Prepare data for weekly ticket sheet
    df_weekly = pd.DataFrame(
        read_tickets_weekly(g[0]),
        columns=["nickname", "tickets_lost", "days_tickets_lost", "full_days_lost"],
    )
    df_weekly = df_weekly.fillna("")

    # Prepare data for monthly ticket sheet
    df_monthly = pd.DataFrame(
        read_tickets_monthly(g[0]),
        columns=["nickname", "tickets_lost", "days_tickets_lost", "full_days_lost"],
    )
    df_monthly = df_monthly.fillna("")

    # Prepare data for weekly points sheet
    df_weekly_points = pd.DataFrame(
        read_member_points(g[0]),
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

    # Batch clear Main and then update
    main.batch_clear(["A2:H51"])
    main.update(range_name="A2:H51", values=df.values.tolist())

    # Batch clear weekly/monthly and then update
    weekly.batch_clear(["A2:D52"])
    weekly.update(range_name="A2:D52", values=df_weekly.values.tolist())
    monthly.batch_clear(["A2:D52"])
    monthly.update(range_name="A2:D52", values=df_monthly.values.tolist())

    # Batch clear Points_weekly, then update
    points_weekly.batch_clear(["A2:G52"])
    points_weekly.update(range_name="A2:G52", values=df_weekly_points.values.tolist())
