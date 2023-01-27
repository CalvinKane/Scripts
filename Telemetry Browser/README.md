# getEthData.py
This script can pull information from CVP telemetry browser. Its currently configured to also output the data into the terminal in a table like look.
## Requirements 
- Python 3.7+
- [Arista CloudVision Python Library](https://github.com/aristanetworks/cloudvision-python)
  - Install via pip: ```pip install --upgrade cloudvision```

## Usage
### Running
From the terminal run:
```bash
python3 getEthData.py
```
### Configuration
[getEthData.py](getEthData.py) has  three variables that the user must set:
1. ```cvp_url```
2. ```deviceID```
3. ```token```

```cvp_url``` needs to be set to the URL of cvp or of CVaaS without the http. i.e. ```www.arista.io```

```deviceID``` needs to be the serial number of the switch you wish to retrive info on

```token``` needs to be a file path that points to a file with the CVP service token in it
- To create a service account token go to ```Settings > Service Account > New Service Account > Generate```
