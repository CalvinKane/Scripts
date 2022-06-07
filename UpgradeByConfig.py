import requests.packages.urllib3
from cvprac.cvp_client import CvpClient
from datetime import datetime
from uuid import uuid4
import re, ssl
ssl._create_default_https_context = ssl._create_unverified_context
requests.packages.urllib3.disable_warnings()

# Set Up Connection to CVP (CVaaS in this example)
cvp_client = CvpClient()
cvaas_token = 'Settings > Service Account > New Or Existing Account > Token'
cvp_client.connect(nodes=['CVP IP/URL'], username='',
                   password='', is_cvaas=True, cvaas_token=cvaas_token)

# Set Up CC Name and UUID
cc_id = str(uuid4())
name = f"Change_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

# Get All Pending Task
tasks = cvp_client.api.get_tasks_by_status('Pending')
upgrade_tasks = []

for task in tasks:
    if task['data']['WORKFLOW_ACTION'] != "Image Push":
        continue

    task_number = task['workOrderId']
    mac = task['workOrderDetails']['netElementId']

    configs = cvp_client.api.get_configlets_by_device_id(mac)
    for config in configs:
        if re.search("MLAG", config['name']):
            upgrade_tasks.append(task_number)

print(task_number)
cvp_client.api.create_change_control_v3(cc_id, name, upgrade_tasks, False)
