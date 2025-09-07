import pandas as pd
import logging
from helper_functions import setup_logging
from enter_data import enter_tb_data

logger = logging.getLogger("guild_data_app")
setup_logging()

try:
    tb_data = pd.read_csv(
        "csv_import/tb_data.csv",
        encoding="utf-8",  # Handle different encodings
        sep=",",  # Specify delimiter (auto-detected by default)
        header=0,  # Row to use as column names (0 = first row)
    )
except FileNotFoundError:
    logger.error("File not found. Check csv_import folder")
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


# To do: Handle renaming of csv file to indicate it processed
# tb_data.csv -> tb_data_imported_{date}_{guild_name}
# get guild_id from join of data inserted in line 42 with players table -> get guild name from guilds table with guild_id
