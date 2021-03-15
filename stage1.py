import requests
import json

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

AUTH = IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def get_alarms():
    url = f"{BASE_URL}/cond/Alarms"
    resp = requests.get(url, auth=AUTH)

    result = []
    for a in resp.json()["Results"]:
        result += [{
            "Description" : a["Description"]
        }]
    return json.dumps(result, indent=2)

def get_infrastructure_summary():
    url = f"{BASE_URL}/compute/PhysicalSummaries"
    resp = requests.get(url, auth=AUTH)

    result = []
    license_tier = ""
    for s in resp.json()["Results"]:
        for tag in s["Tags"]:
            if tag["Key"] == "Intersight.LicenseTier":
                license_tier = tag["Value"]
        result += [{
            "Management mode" : s["ManagementMode"],
            "Management IP" : s["MgmtIpAddress"],
            "Name" : s["Name"],
            "Number of CPUs" : s["NumCpus"],
            "Number of CPU cores" : s["NumCpuCores"],
            "Admin power state" : s["AdminPowerState"],
            "Firmware" : s["Firmware"],
            "Model" : s["Model"],
            "Serial" : s["Serial"],
            "License tier" : license_tier,
        }]
    return json.dumps(result, indent=2)

def get_hcl_status():
    url = f"{BASE_URL}/cond/HclStatuses"
    resp = requests.get(url, auth=AUTH)

    result = []
    for h in resp.json()["Results"]:
        result += [{
            "HCL OS vendor" : h["HclOsVendor"],
            "HCL OS version" : h["HclOsVersion"],
        }]
    return json.dumps(result, indent=2)

def get_clusters():
    url = f"{BASE_URL}/kubernetes/Clusters"
    resp = requests.get(url, auth=AUTH)

    result = []
    for h in resp.json()["Results"]:
        result += [{
            "Name" : h["Name"],
        }]
    return json.dumps(result, indent=2)

def get_nb_deployments():
    url = f"{BASE_URL}/kubernetes/Deployments"
    resp = requests.get(url, auth=AUTH)

    return len(resp.json()["Results"])

if __name__ == "__main__":
    f = open("stage1.json", 'w')

    f.write(f"Alarm descriptions:\n{get_alarms()}\n\n")
    f.write(f"Physical infrastructure summary:\n{get_infrastructure_summary()}\n\n")
    f.write(f"HCL compliance:\n{get_hcl_status()}\n\n")
    f.write(f"Kubernetes clusters:\n{get_clusters()}\n\n")
    f.write(f"Number of Kubernetes deployments:\n{get_nb_deployments()}\n\n")
