import requests
from typing import Dict, Any


def post_request(url: str, data: Dict[str, Any], timeout: int = 30):
    try:
        response = requests.post(url, json=data, timeout=timeout)

        if response.status_code == 200:
            content = response.json()
            return content
        else:
            print("Error:", response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
