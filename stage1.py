import requests
import json

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

AUTH = IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def write_is_info(name, endpoint):
    url = f"{BASE_URL}{endpoint}"
    resp = requests.get(url, auth=AUTH)
    return f"{name}:\n{json.dumps(resp.json(), indent=2)}\n\n"

if __name__ == "__main__":
    f = open("stage1.json", 'w')

    f.write(write_is_info("Alarms", "/cond/Alarms"))
    f.write(write_is_info("Physical Infrastructure summary", "/compute/PhysicalSummaries"))
    f.write(write_is_info("HCL statuses", "/cond/HclStatuses"))
    f.write(write_is_info("Kubernetes clusters", "/kubernetes/Clusters"))
    f.write(write_is_info("Kubernetes deployments", "/kubernetes/Deployments"))
