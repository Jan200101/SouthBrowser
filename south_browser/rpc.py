import json

from requests import post
from time import time, sleep

_PAYLOAD_ID = 0
LOCAL_RPC = "http://localhost:26503/rpc"

def cmd(method: str, params = None):
    global _PAYLOAD_ID
    _PAYLOAD_ID += 1

    payload = {
        "jsonrpc": "2.0",
        "id": int(time()),
        "method": method
    }

    if params is not None:
        payload["params"] = params

    r = post(LOCAL_RPC, data=json.dumps(payload))

    if r.status_code != 200:
        raise Exception(r.text)

    data = r.json()
    return data

def NSRequestServerList():
    return cmd("execute_squirrel", {
        "code": "return NSRequestServerList()"
    })["result"]

def NSGetServerCount(repeat: bool = True):
    data = cmd("execute_squirrel", {
        "code": "return NSGetServerCount()"
    })

    c = data["result"]

    if not c and repeat:
        NSRequestServerList()
        sleep(1) # give it a second to popualte
        return NSGetServerCount(False)

    return c

def NSGetGameServers():
    # work around Squirrel closure bullshit
    server_count = NSGetServerCount()
    if not server_count:
        return []

    primret = []
    for c in range(server_count):
        primret.append(f"[s[{c}].index, s[{c}].id, s[{c}].name, s[{c}].description, s[{c}].map, s[{c}].playlist, s[{c}].playerCount, s[{c}].maxPlayerCount, s[{c}].requiresPassword, s[{c}].region]")

    ret = "[" + ",".join(primret) + "]"

    return cmd("execute_squirrel", {
        "code": f"array<ServerInfo> s = NSGetGameServers()\nreturn {ret}"
    })["result"]


def NSTryAuthWithServer(index: int, password: str = None):
    if password is None:
        password = ""

    return cmd("execute_squirrel", {
        "code": f"return NSTryAuthWithServer({index}, {json.dumps(password)})"
    })["result"]

def NSWasAuthSuccessful():
    return cmd("execute_squirrel", {
        "code": "return NSWasAuthSuccessful()"
    })["result"]

def NSConnectToAuthedServer():
    return cmd("execute_squirrel", {
        "code": "return NSConnectToAuthedServer()"
    })["result"]
