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
        error_str = "Error: Check .env file. %s should not be None", key
        logger.exception(error_str)
        raise ValueError(error_str)
    return value


def check_none(possible_none_value, error_str: str) -> str:
    if possible_none_value is None:
        logger.exception(error_str)
        raise ValueError(error_str)
    return possible_none_value


def is_list_or_tuple_instance(possible_tuple):
    if isinstance(possible_tuple, (list, tuple)):
        return possible_tuple
    else:
        logger.exception(
            "read_players is not returning a list or tuple. Check read_players function"
        )
