import json
import urllib3
from concurrent.futures import as_completed
from requests_futures.sessions import FuturesSession
import requests
import pkgutil
from loguru import logger
import time

def _get_instance_ids_from_names(url,headers,names:list):
    session = FuturesSession()
    endpoint = "/api/instances"
    ids = []
    futures=[session.get(f'{url}{endpoint}?name={n}',headers=headers,verify=False) for n in names]
    for future in as_completed(futures):
        resp = future.result()
        if "200" in str(resp):
            i = resp.json()["instances"][0]
            ids.append(i["id"])
    return(ids)

def _tag_xaas_with_instance_ids(url,headers,target_id,instance_ids:list):
    endpoint = "/api/instances"
    payload = {'instance':{'addTags':[{'name': 'Lab Instance IDs','value': instance_ids}]}}
    try:
        logger.info('Attempting to add tag to the instance')
        resp = requests.put(f'{url}{endpoint}/{target_id}', headers=headers, verify=False, data=json.dumps(payload))
        return(resp)
    except Exception as e:
        logger.error(f'Something went wrong inthe operation')


