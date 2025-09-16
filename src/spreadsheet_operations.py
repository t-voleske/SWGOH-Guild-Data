import os
from pathlib import Path
from functools import cache
import logging
import gspread
from gspread.utils import ValueRenderOption
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from src.helper_functions import check_none_str, setup_logging

logger = logging.getLogger("guild_data_app")
setup_logging()
load_dotenv()


filepath: str = check_none_str(
    os.getenv("FILEPATH_CREDENTIALS"),
    "FILEPATH_CREDENTIALS should not be None. Check .env file",
)
gc = gspread.service_account(filename=Path(filepath))


@cache
def _get_spreadsheet_values_cached(
    g_config_tuple: tuple, worksheet_name: str
) -> list[list] | None:
    # Convert back to list for internal use
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
    return _get_spreadsheet_values_cached(tuple(g_config), worksheet_name)


def check_order(g_config: list, worksheet_name: str) -> str:
    table_data: list[list] | None = get_spreadsheet_values(g_config, worksheet_name)
    if table_data is not None:
        columns = table_data.pop(0)
        table_df = pd.DataFrame(table_data, columns=columns)
        table_order = table_df.iloc[:2, -1].tolist()
        return f"{table_order[0]} {table_order[1]}"
    else:
        return "nickname ASC"


def update_not_needed(
    g_config: list, worksheet_name: str, database_df: pd.DataFrame
) -> bool:
    table_data: list[list] | None = get_spreadsheet_values(g_config, worksheet_name)
    if table_data is not None:
        columns = table_data.pop(0)
        table_df = pd.DataFrame(table_data, columns=columns)
        table_order = table_df.iloc[:2, -1].tolist()
        table_df = table_df.iloc[:, :-1]
        logger.info("Data is ordered by %s %s", table_order[0], table_order[1])
        logger.debug("Worksheet Dataframe:")
        logger.debug(table_df)
        logger.debug("\n Database Dataframe:")
        logger.debug(database_df)
        data_equal_check = np.array_equal(table_df.values, database_df.values)
        # data_equal_check = table_df.iloc[:, 0:2].equals(database_df.iloc[:, 0:2])
        logger.info("\n The data is equal: %s", data_equal_check)
        return data_equal_check
    else:
        return False


def write_to_sheet(
    g_config: list, worksheet_name: str, data_df: pd.DataFrame, worksheet_range: str
) -> None:
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
