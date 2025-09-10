import logging
from pathlib import Path
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from helper_functions import setup_logging
from enter_data import enter_tb_data
from read_data import get_guild_from_nickname


load_dotenv()
csv_import_folder_filepath: str = str(os.getenv("CSV_IMPORT_FOLDER_FILEPATH"))

logger = logging.getLogger("guild_data_app")
setup_logging()


def get_guild_random(input_list: list[list]) -> str:
    guild_names = []
    for x in np.random.randint(0, len(input_list), size=10):
        guild_names.append(get_guild_from_nickname(input_list[x][0]))
    guild_names_set = set(guild_names)
    if len(guild_names_set) == 1:
        return guild_names[0]
    else:
        logger.info(
            "More than one guild recognized from "
            "the nicknames in TB data. Did players change guild recently?"
        )
        return max(guild_names_set, key=guild_names.count)


try:
    tb_data = pd.read_csv(
        f"{csv_import_folder_filepath}tb_data.csv",
        encoding="utf-8",
        sep=",",
        header=0,
    )
except FileNotFoundError:
    logger.error("File not found. Check csv_import folder")
    sys.exit()
except pd.errors.EmptyDataError:
    logger.error("CSV file is empty")
except pd.errors.ParserError:
    logger.error("Error parsing CSV")

logger.debug(tb_data.head())
deployed_gp_df = tb_data.filter(regex=r"Name|Deployed GP")
combat_attempts_df = tb_data.filter(regex=r"Name|Combat Attempts")
summed_data = tb_data.filter(regex=r"Name|Total Territory Points|Combat Waves")
summed_data["Combat Attempts"] = combat_attempts_df.select_dtypes(include="number").sum(
    axis=1
)
summed_data["Wave Success Ratio"] = [
    None if y == 0 else round(x / (y * 2), 2)
    for x, y in zip(summed_data["Combat Waves"], summed_data["Combat Attempts"])
]
summed_data["Missed Phases"] = (
    deployed_gp_df.select_dtypes(include="number") == 0
).sum(axis=1)
logger.debug(summed_data)
summed_data_list = summed_data.values.tolist()
logger.info("summed_data_list")
logger.info(summed_data_list)

enter_tb_data(summed_data_list)

timestamp = datetime.now().strftime("%d-%m-%Y")
guild = get_guild_random(summed_data_list)
logger.info("The guild is: %s and the date is %s", guild, timestamp)

try:
    Path(f"{csv_import_folder_filepath}tb_data.csv").rename(
        f"{csv_import_folder_filepath}tb_data_imported_{timestamp}_{guild}.csv"
    )
    logger.info("File renamed successfully")
except FileNotFoundError:
    logger.error("File not found")
