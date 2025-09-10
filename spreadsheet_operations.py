import os
from pathlib import Path
import gspread
import pandas as pd
from dotenv import load_dotenv
from helper_functions import check_none_str, setup_logging
import logging

logger = logging.getLogger("guild_data_app")
setup_logging()
load_dotenv()


filepath: str = check_none_str(
    os.getenv("FILEPATH_CREDENTIALS"),
    "FILEPATH_CREDENTIALS should not be None. Check .env file",
)
gc = gspread.service_account(filename=Path(filepath))


def write_to_sheet(
    g_config: list, worksheet_name: str, data_df: pd.DataFrame, worksheet_range: str
) -> None:
    logger.info(
        "Writing to sheet %s for guild %s in range %s",
        worksheet_name,
        g_config[1],
        worksheet_range,
    )
    logger.info(g_config)
    sheet = gc.open(g_config[3])
    # worksheet_check = gc.worksheets()
    # if worksheet_name is not in worksheet_check:
    #    logger.warning("Worksheet %s not found. Skipping worksheet.")
    #    return
    try:
        active_worksheet = sheet.worksheet(worksheet_name)
        logger.debug(data_df)

        active_worksheet.batch_clear([worksheet_range])
        active_worksheet.update(
            range_name=worksheet_range, values=data_df.values.tolist()
        )
    except gspread.exceptions.SpreadsheetNotFound as e:
        logger.error(e)
        logger.debug("Spreadsheet %s is non-existent or inaccessible", gc)
    except gspread.exceptions.WorksheetNotFound:
        logger.warning("Worksheet %s is non-existent or inaccessible", worksheet_name)
    except gspread.exceptions.GSpreadException as e:
        logger.error(
            "Exeption %s was triggered while trying to write to worksheet %s",
            e,
            worksheet_name,
        )
