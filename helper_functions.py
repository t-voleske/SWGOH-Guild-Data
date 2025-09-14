import json
import logging.config
import logging
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("guild_data_app")
logger_filepath: str = str(os.getenv("LOGGER_FILEPATH"))


def setup_logging():
    config_file = Path(logger_filepath)
    try:
        with open(config_file, encoding="utf-8") as f_in:
            config = json.load(f_in)
        logging.config.dictConfig(config)
    except FileNotFoundError:
        # Fallback to basic logging if config file doesn't exist
        logging.basicConfig(level=logging.INFO)
        logging.warning(
            "Logging config file %s not found, using basic config", config_file
        )
    except (json.JSONDecodeError, KeyError) as e:
        logging.basicConfig(level=logging.INFO)
        logging.error("Error loading logging config: %s", e)


setup_logging()


def get_env(key: str) -> str:
    value = os.getenv(key)
    if value is None:
        logger.exception("Error: Check .env file. %s should not be None", key)
        raise ValueError(f"Error: Check .env file. {key} should not be None")
    return value


def check_none_str(possible_none_value, error_str: str) -> str:
    if possible_none_value is None:
        logger.exception(error_str)
        raise ValueError(error_str)
    if type(possible_none_value) is not str:
        logger.exception(
            "possible_none_value should be type str. Use the check_none function of the right type instead!"
        )
        raise TypeError(
            "possible_none_value should be type str. Use the check_none function of the right type instead!"
        )
    return possible_none_value


def check_none_list(possible_none_value, error_str: str) -> list:
    if possible_none_value is None:
        logger.exception(error_str)
        raise ValueError(error_str)
    if type(possible_none_value) is not list:
        logger.exception(
            "possible_none_value should be type list. Use the check_none function of the right type instead!"
        )
        raise TypeError(
            "possible_none_value should be type list. Use the check_none function of the right type instead!"
        )
    return possible_none_value


def is_list_or_tuple_instance(input_value):
    if isinstance(input_value, (list, tuple)):
        return input_value
    else:
        logger.exception("Input is not a list or tuple. Check input function!")
        raise TypeError("Input is not a list or tuple. Check input function!")


def floatify(x: int) -> float | str:
    if x == "":
        return "-"
    return float(x)
