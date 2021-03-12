import requests
import json

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

AUTH = IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def get_ntp_policies():
    url = f"{BASE_URL}/ntp/Policies"
    resp = requests.get(url, auth=AUTH)
    return resp.json()

if __name__ == "__main__":
    f = open("stage0.json", 'w')
    f.write(json.dumps(get_ntp_policies(), indent=2))
