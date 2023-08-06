import requests

def get_token(url: str, password: str):
    
    url = url + "/auth"

    result = requests.post(url=url, data={ "password": password })
    
    if result.status_code == 200:
        return result.json()["data"]
    return None