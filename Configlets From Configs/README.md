# Configlet Automation
### The main goal of this script is to automate turning a switch config into configlets.

# Requirements 
- Python >= 3.6 [^version]
- [Config Parser](./ConfigParser.py), included in this folder

[^version]: Developed with Python 3.8.9
# Usage
## Running 
Run [DivideConfigs.py](./DivideConfigs.py) in a terminal:
```bash
python3 DivideConfigs.py
```
By default it looks for configs in a relative directory called "configs" and will output the configlets in a subfolder of that directory called "configlets." These are easily changeable by modifying the ```config_directory``` and ```output_directory``` variables in the user input section of the script.

## Configuration
[DivideConfigs.py](./DivideConfigs.py) has three variables that the user can control:
1. ```config_directory```
2. ```output_directory```
3. ```configlets```

```config_directory``` and ```output_directory``` were explained above.

```configlets``` is a dictionary where the key will be appended to the config name and the value is a list of what sections you want in that configlet. Example:
```Python
configlets = {
    'Base': ['hostname', 'spanning tree', 'mlag'],
}
```
In this example the configlet name will be ```InputConfigName-Base.cfg``` and will have the hostname, spanning tree, and mlag configs within it.

The available sections are defined by the keys in ```cfg_dict``` within [Config Parser](./ConfigParser.py). Feel free to add your own if it's missing one you want.
