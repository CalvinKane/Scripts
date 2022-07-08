#!/usr/bin/env python3
import pathlib
import ConfigParser

### User Input
config_directory = './configs'
output_directory = './configs/configlets/'

configlets = {
    'Base': ['hostname', 'spanning tree', 'mlag'],
    'IP': ['ip route', 'ip routing', 'ip virtual-router'],
    'VRF': ['vrf'],
    'Interfaces': ['interface', 'vlan']
}
###

def write_config_to_file(conf: dict):
    for configlet in configlets:
        print(f'=== Making configlet for: {configlet} ===\n')
        
        config = ''
        for section in configlets[configlet]:
            config += conf[section]
        
        configlet_name = f'{output_directory}{path.name.split(".")[0]}-{configlet}.cfg'
        with open(configlet_name, 'w') as configlet_file:
            configlet_file.write(config)

if __name__ == '__main__':
    pathlib.Path(output_directory).mkdir(parents=True, exist_ok=True)
    for path in pathlib.Path(config_directory).iterdir():
        if path.is_file() and path.suffix == '.cfg':
            print(f'Opening file: {path.name}\n')
            
            with open(path, 'r') as cfg:
                conf = ConfigParser.Parse(cfg)
                write_config_to_file(conf)