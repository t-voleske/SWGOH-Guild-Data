import os
from pathlib import Path
from functools import cache, wraps
import time
import logging
from typing import Callable
import gspread
from gspread.utils import ValueRenderOption
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from .helper_functions import check_none_str, setup_logging

logger = logging.getLogger("guild_data_app")
setup_logging()
load_dotenv()



filepath: str = check_none_str(
    os.getenv("FILEPATH_CREDENTIALS"),
    "FILEPATH_CREDENTIALS should not be None. Check .env file",
)
gc = gspread.service_account(filename=Path(filepath))


def rate_limit(calls_per_minute: float):
    """
    Rate limit function to prevent rate limiting by spreadsheet API, that could abort the program
    """
    min_interval = 60.0 / calls_per_minute 
    last_called = [0.0]
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret_func = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret_func
        return wrapper
    return decorator

@rate_limit(calls_per_minute=40)
@cache
def _get_spreadsheet_values_cached(
    g_config_tuple: tuple, worksheet_name: str
) -> list[list] | None:
    """
    Cached spreadsheet read function to prevent rate limiting by spreadsheet API
    """
    # Convert back to list for further processing
    g_config = list(g_config_tuple)

    logger.info(
        "Getting values of %s for guild %s",
        worksheet_name,
        g_config[1],
    )
    logger.info(g_config)
    sheet = gc.open(g_config[3])
    try:
        active_worksheet = sheet.worksheet(worksheet_name)
        values_in_sheets: list[list] = active_worksheet.get_all_values(
            value_render_option=ValueRenderOption.unformatted
        )
        return values_in_sheets
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


def get_spreadsheet_values(g_config: list, worksheet_name: str) -> list[list] | None:
    """
    Wrapper for the cached spreadsheet read function
    """
    return _get_spreadsheet_values_cached(tuple(g_config), worksheet_name)


def check_order(g_config: list, worksheet_name: str) -> str:
    """
    Checks the order settings for a worksheet by reading them from the spreadsheet
    """
    table_data: list[list] | None = get_spreadsheet_values(g_config, worksheet_name)
    if table_data is not None:
        table_df = pd.DataFrame(table_data)
        table_order = table_df.iloc[0:3, -1].tolist()
        logging.info("table_order")
        logging.info(table_order)
        return f"{table_order[1]} {table_order[2]}"
    else:
        return "nickname" "ASC"
    
def check_timeframe(g_config: list, worksheet_name: str) -> str:
    """
    Checks the timeframe settings for a worksheet by reading them from the spreadsheet
    """
    table_data: list[list] | None = get_spreadsheet_values(g_config, worksheet_name)
    if table_data is not None:
        table_df = pd.DataFrame(table_data)
        table_timeframe = table_df.iloc[3, -1]
        logging.info("table_timeframe")
        logging.info(table_timeframe)
        return f"{table_timeframe}"
    else:
        return "two_weeks"


def update_not_needed(
    g_config: list, worksheet_name: str, database_df: pd.DataFrame
) -> bool:
    """
    Checks whether an update for the table is needed to reduce API requests
    """
    table_data: list[list] | None = get_spreadsheet_values(g_config, worksheet_name)
    if table_data is not None:
        columns = table_data.pop(0)
        table_df = pd.DataFrame(table_data, columns=columns)

        if len(table_df) >= 2 and len(table_df.columns) > 0:
            table_order = table_df.iloc[:2, -1].tolist()
        elif len(table_df) == 1 and len(table_df.columns) > 0:
            table_order = [table_df.iloc[0, -1], ""]  # Pad with empty string
        else:
            table_order = ["nickname", "ASC"]  # Default empty values
            logger.warning("Insufficient data in spreadsheet for ordering info")
            

        if len(table_df.columns) > 0:
            table_df = table_df.iloc[:, :-1]
        
        if len(table_order) >= 2 and table_order[0] and table_order[1]:
            logger.info("Data is ordered by %s %s", table_order[0], table_order[1])
        elif len(table_order) >= 1 and table_order[0]:
            logger.info("Data is ordered by %s", table_order[0])
        else:
            logger.info("No ordering information found in spreadsheet")
        
        logger.debug("Worksheet Dataframe:")
        logger.debug(table_df)
        logger.debug("\n Database Dataframe:")
        logger.debug(database_df)
        data_equal_check = np.array_equal(table_df.values, database_df.values)

        logger.info("\n The data is equal: %s", data_equal_check)
        return data_equal_check
    else:
        return False


def write_to_sheet(
    g_config: list, worksheet_name: str, data_df: pd.DataFrame, worksheet_range: str
) -> None:
    """
    Writes data to worksheet in spreadsheet at given range
    """
    if update_not_needed(g_config, worksheet_name, data_df):
        logger.info(
            "Writing to sheet %s for guild %s not needed. Information is up to date.",
            worksheet_name,
            g_config[1],
        )
        return
    logger.info(
        "Writing to sheet %s for guild %s in range %s",
        worksheet_name,
        g_config[1],
        worksheet_range,
    )
    logger.info(g_config)
    sheet = gc.open(g_config[3])

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
