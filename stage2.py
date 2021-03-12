import requests
import json
import datetime

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

ACI_SESSION = get_authenticated_aci_session(config['ACI_USER'], config['ACI_PASSWORD'], config['ACI_BASE_URL'])

def get_health_score(tenant):
    url = f"{config['ACI_BASE_URL']}/api/node/mo/uni/{tenant}.json?query-target=self&rsp-subtree-include=health"
    resp = ACI_SESSION.get(url)
    return [resp.json()["imdata"][0]["fvTenant"]["children"][0]["healthInst"]["attributes"]["cur"], \
        resp.json()["imdata"][0]["fvTenant"]["children"][0]["healthInst"]["attributes"]["maxSev"]]

def get_health_overview():
    url = f"{config['ACI_BASE_URL']}/api/class/fabricHealthTotal.json"
    resp = ACI_SESSION.get(url)

    return resp.json()

def get_tenants():
    url = f"{config['ACI_BASE_URL']}/api/class/fvTenant.json?rsp-subtree-include=health"
    resp = ACI_SESSION.get(url)

    result = []
    for tenant in resp.json()["imdata"]:
        dn = tenant["fvTenant"]["attributes"]["dn"]
        result += [dn[str.index(dn,"tn-"):]]
    return result

if __name__ == "__main__":
    TENANTS = get_tenants()

    with open("stage2.csv", "w") as f:
        f.write("Tenant; Timestamp; Health score; Maximum severity\n")
        for t in TENANTS:
            health = get_health_score(t)
            f.write(f"{t}; {datetime.datetime.now().isoformat()}; {health[0]}; {health[1]}\n")