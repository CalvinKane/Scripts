from cloudvision.Connector.grpc_client import GRPCClient, create_query
from cloudvision.Connector.codec import Wildcard
import re

### User Input
cvp_url = "CVP URL"
deviceID = ""
token = "token_file_path"
###

# function based on https://github.com/aristanetworks/cloudvision-python/blob/trunk/examples/Connector/get_intf_status.py
def get(client, dataset, pathElts):
    ''' Returns a query on a path element'''
    query = [
        create_query([(pathElts, [])], dataset)
    ]

    out = {}
    for batch in client.get(query):
        for notif in batch["notifications"]:
            try:
                out[notif['path_elements'][-1]].update(notif['updates'])
            except KeyError:
                out[notif['path_elements'][-1]] = notif['updates']
                continue
    return out

# https://stackoverflow.com/questions/4836710/is-there-a-built-in-function-for-string-natural-sort
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key=alphanum_key)

def print_header():
    print('{:^14} | {:^11} | {:^10} | {:^10} | {:^12} | {:^12} | {}'.format("Interface", "Access Vlan", "Desc", "Port Mode", "Speed", "Admin Status", "OperStaus"))

def retrive_value(dict: dict, dict_index: list):
    try:
        out = dict
        for index in dict_index:
            out = out[index]
        return out
    except KeyError:
        return ' - '

def get_multiple_paths(client, deviceID, *paths):
        out = {}
        for path in paths:
            result = get(client, deviceID, path)
            for key, value in result.items():
                try:
                    out[key].update(value)
                except KeyError:
                    out[key] = value
                    continue
        return out

# /Sysdb/interface/config/eth/phy/slice/1/intfConfig
config = [
    "Sysdb",
    "interface",
    "config",
    "eth",
    "phy",
    "slice",
    "1",
    "intfConfig",
    Wildcard()
]
# /Sysdb/interface/status/eth/phy/slice/1/intfStatus
status = [
    "Sysdb",
    "interface",
    "status",
    "eth",
    "phy",
    "slice",
    "1",
    "intfStatus",
    Wildcard()
]
#/Sysdb/bridging/config/switchIntfConfig/
bridging = [
    "Sysdb",
    "bridging",
    "config",
    "switchIntfConfig",
    Wildcard()
]
# Path used by dashboard /Sysdb/bridging/input/config/cli/switchIntfConfig
# /Sysdb/bridging/switchIntfConfig/switchIntfConfig/
vlan = [
    "Sysdb",
    "bridging",
    "switchIntfConfig",
    "switchIntfConfig",
    Wildcard()
]

def main(apiserverAddr, deviceID, token=None):
    with GRPCClient(apiserverAddr, token=token) as client:
        data = get_multiple_paths(client, deviceID, config, status, bridging, vlan)

    print_header()
    sorted_index = natural_sort(data.keys())
    for index in sorted_index:
        interface = index
        value = data[index]
        print(f"\
{interface:<14} | \
{retrive_value(value, ['accessVlan', 'value']):^11} | \
{retrive_value(value, ['description']):<10} | \
{retrive_value(value, ['switchportModeAndNativeVlan', 'switchportMode', 'Name']):^10} | \
{retrive_value(value, ['speedEnum', 'Name']):<12} | \
{retrive_value(value, ['enabledStateLocal', 'Name']):^12} | \
{retrive_value(value, ['operStatus', 'Name'])}")

if __name__ == "__main__":
    main(cvp_url, deviceID, token)