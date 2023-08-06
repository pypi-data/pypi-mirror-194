import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_instance_existence(url,headers,ids):
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.get(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            instance = resp.json()
            id = instance["instance"]["id"]
            instances.append(id)
    return(instances)

def unlock_instances(url,headers,ids:list):
    logger.info(f'Attempting to unlock instances: {ids}')
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.put(f'{url}{endpoint}{i}/unlock', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            for k in resp["results"].keys():
                logger.info(f'Instance {k} unlocked')
                instances.append(k)
    return(instances)

def delete_instances(url,headers,ids:list):
    session = FuturesSession() 
    instances = []
    endpoint = "/api/instances/"
    futures=[session.delete(f'{url}{endpoint}{i}', headers=headers, verify=False) for i in ids]
    for future in as_completed(futures):
        resp = future.result().json()
        if resp["success"]:
            logger.info(f'Successfully initiated teardowm of instance')
        return(resp)

def delete_classroom_labs(url,headers,master_instance_id,tag_name):
    endpoint = "/api/instances"
    tags = requests.get(f'{url}{endpoint}/{master_instance_id}',headers=headers, verify=False).json()["instance"]["tags"]
    for t in tags:
        if tag_name in t["name"]:
            logger.info(f'Found the defined tag.')
            ids = t["value"]
            ids = json.loads(ids)
            logger.info(f'Unlocking the instances.')    
            unlock_instances(url,headers,ids)
            logger.info(f'Deleting the instances')
            delete_instances(url,headers,ids)
            return()