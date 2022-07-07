#!/usr/bin/env python3
import pathlib
import AristaParser

configlets = {
    'Base': ['hostname', 'spanning tree', 'mlag'],
    'IP': ['ip route', 'ip routing', 'ip virtual-router'],
    'VRF': ['vrf'],
    'Interfaces': ['interface', 'vlan']
}

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
    directory = './configs'
    output_directory = './configs/configlets/'

    for path in pathlib.Path(directory).iterdir():
        if path.is_file() and path.suffix == '.cfg':
            print(f'Opening file: {path.name}\n')
            
            with open(path, 'r') as cfg:
                conf = AristaParser.Parse(cfg)
                write_config_to_file(conf)