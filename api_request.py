import requests

def post_request(str, d):
    url = str
    data = d
    headers = {
			'Content-Type': 'application/json'
	}
    try:
        response = requests.post(url, json=data)

        if response.status_code == 200:
            content = response.json()
            return content
        else:
            print('Error:', response.status_code)
            return None
    except requests.exceptions.RequestException as e:
        print('Error:', e)
        return None
