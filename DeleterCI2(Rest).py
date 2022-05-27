#coding=utf-8

import rest_requests as requests
import logger
from appilog.common.system.types.vectors import ObjectStateHolderVector


def execute_post(url, urn, headers, body):
    uri = url + urn
    r = requests.post(uri, headers=headers, json=body, verify=False)
    res = r.json()
    return res


def authenticate(url):
    urn = "/rest-api/authenticate"
    headers = {"Content-Type": "application/json"}
    body={"username": "user", "password": "passwd", "clientContext": 1}
    out = execute_post(url, urn, headers, body)
    # out = r.json()
    token = out["token"]
    headers = {"Authorization": "Bearer " + token, "Content-Type": "application/json; charset=utf-8"}
    return headers

"""
# Создание пустых КЕ 
def creating():
    for i in range(5000):
        body = {"cis": [{"ucmdbId": "1",
                         "type": "node",
                         "properties": {"name": "test_node{}".format(i)},
                         "attributesQualifiers": {}
                         }]}
        res = execute_post("/rest-api/dataModel", headers, body)
"""


def DiscoveryMain(Framework):
    OSHVResult = ObjectStateHolderVector()
    try:
        #change hardcode to get credentials
        protocol = "https"
        port = "8443"
        host = "10.3.6.78"

        url = protocol + '://' + host + ":" + port
        headers = authenticate(url)

        body = {"name": "get_nodes_to_delete",
            "nodes": [{"queryIdentifier": "nodes",
                    "type": "node",
                    "visible": True,
                    "includeSubtypes": True,
                    "layout": ["display_label", "global_id"],
                    "ids": [],}, ],}

        res = execute_post(url, "/rest-api/topologyQuery/", headers, body)
        for ci in res["cis"]:
            ciId = ci["ucmdbId"]
            del_ci_uri = protocol + '://' + host + ":" + port + "/rest-api/dataModel/ci/" + ciId
            r = requests.delete(del_ci_uri, headers=headers, verify=False)
            if r.status_code != 200:
                res = r.json()
    except Exception, e:
        logger.debug("smth was wrong ", e)


    return OSHVResult
