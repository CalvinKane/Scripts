import requests.packages.urllib3
from cvprac.cvp_client import CvpClient
from datetime import datetime
from uuid import uuid4
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

# Set Up Connection to CVP (CVaaS in this example)
cvp_client = CvpClient()
cvaas_token = 'Settings > Service Account > New Or Existing Account > Token'
cvp_client.connect(nodes=['CVP IP/URL'],
                   username='', password='', is_cvaas=True, cvaas_token=cvaas_token)

# Set Up CC Name and UUID
a_cc_id = str(uuid4())
a_cc_name = f"Change_A_Side_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
b_cc_id = str(uuid4())
b_cc_name = f"Change_B_Side_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

a_side_tasks = []
b_side_tasks = []


def get_device_ids_by_tag(client):
    tag_url = '/api/resources/tag/v1/DeviceTagAssignmentConfig/all'
    response = client.get(tag_url)
    data = response['data']

    a = []
    b = []
    for tag in data:
        tag_keys = tag['result']['value']['key']
        if tag_keys['label'] == 'MLAG':
            if tag_keys['value'] == 'A':
                a.append(tag_keys['deviceId'])
            elif tag_keys['value'] == 'B':
                b.append(tag_keys['deviceId'])
            else:
                print(f"Unexpected value: {tag_keys['value']}")

    return a, b


def filter_tasks(tasks):
    for task in tasks:
        if task['data']['WORKFLOW_ACTION'] != "Image Push":
            continue

        task_number = task['workOrderId']
        serial = task['workOrderDetails']['serialNumber']

        if serial in a_side_mlag:
            a_side_tasks.append(task_number)
        elif serial in b_side_mlag:
            b_side_tasks.append(task_number)
        else:
            continue


def create_cc(cc_id, cc_name, tasks, sequential: bool = True):
    if len(tasks) == 0:
        print(f"Skipping Change Control For: {cc_name} - Task List Was Empty")
        return

    cvp_client.api.create_change_control_v3(
        cc_id, cc_name, tasks, sequential)
    print(f"Created {cc_name} With Task(s): {tasks}")


if __name__ == '__main__':
    print("Getting Device IDs By Tag...\n")
    a_side_mlag, b_side_mlag = get_device_ids_by_tag(cvp_client)

    print("Getting All Pending Upgrade Task...\n")
    tasks = cvp_client.api.get_tasks_by_status('Pending')
    filter_tasks(tasks)

    print("Creating Change Control(s)..\n")
    create_cc(a_cc_id, a_cc_name, a_side_tasks, False)
    create_cc(b_cc_id, b_cc_name, b_side_tasks, False)
