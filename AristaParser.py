import re
from io import TextIOWrapper

cfg_dict = {
    'hostname': re.compile(r'^(hostname.*\n)'),
    'spanning tree': re.compile(r'(?:^|no )(spanning-tree.*\n)'),
    'vrf': re.compile(r'^(vrf.*\n)'),
    'mlag': re.compile(r'^(mlag.*\n)'),
    'ip route': re.compile(r'^(ip route.*\n)'),
    'ip routing': re.compile(r'(?:^|^no )(ip routing.*\n)'),
    'ip virtual-router': re.compile(r'^(ip virtual-router.*\n)'),
    'interface': re.compile(r'^(interface.*\n)'),
    'vlan': re.compile(r'^(vlan.*\n)'),
}

def Parse(cfg: TextIOWrapper):
    """
    Input File

    Output Dict
    """
    output = {}
    cur_line = cfg.readline()
    while cur_line:
        if '!' in cur_line:
            cur_line = cfg.readline()
            continue

        key, configuration, cur_line = regex_line(cur_line, cfg)
        if configuration:
            if key in output:
                output[key] += configuration
            else:
                output[key] = configuration

    return output

def regex_line(cur_line, cfg):
    for key, rx in cfg_dict.items():
        match = rx.search(cur_line)
        if match:
            configuration = match[0]
            cur_line = cfg.readline()
            while cur_line:
                if ' ' in cur_line[0]:
                    configuration += cur_line
                    cur_line = cfg.readline()
                else:
                    return key, configuration, cur_line
    cur_line = cfg.readline()
    return None, None, cur_line
