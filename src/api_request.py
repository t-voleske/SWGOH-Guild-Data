import logging
from typing import Dict, Any
import requests
from .helper_functions import setup_logging

logger = logging.getLogger("guild_data_app")


def post_request(url: str, data: Dict[str, Any], timeout: int = 30):
    setup_logging()
    try:
        response = requests.post(url, json=data, timeout=timeout)

        if response.status_code == 200:
            content = response.json()
            return content
        else:
            logger.error(response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return None
