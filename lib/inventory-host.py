#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import os
import sys
import getpass
from commands import getoutput
from ansible.errors import AnsibleError

# INV_PATH = os.getenv('INVENTORY_HOST_FILE')
bin_path = sys.path[0]
INV_PATH = bin_path[:-3] + "hosts"

try:
    import json
except ImportError:
    import simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

# nc_inv = {'colynn-test2': {'ansible_ssh_host': '172.31.3.154', 'ansible_ssh_port': '22'}}

nc_inv = OrderedDict()
inv = open(INV_PATH, 'r')
for line in inv:
    if ( line != '' or line != '\n' ) and (line.startswith('#') == False):
        vars = line.split()
        if len(vars) < 4:
            raise AnsibleError("this line has some missed,\n" + line + "eg:\nexample-web1 ansible_host=13.14.52.11 ansible_port=22 ansible_user=example-user")
            sys.exit(1)
        host_info = {}
        host_info["ansible_host"] = vars[1].split('=')[1]
        host_info["ansible_port"] = vars[2].split('=')[1]
        host_info["ansible_user"] = vars[3].split('=')[1]
        nc_inv[vars[0]] = host_info
inv.close()

def Usage():
    print "Usage:  %s --list" % sys.argv[0]
    sys.exit(1)

def get_srv_pass(hostname):
    """
    ncadmin@srv-name's password:
    """
    password = getpass.getpass(nc_inv[hostname]['ansible_user'] + "@" + hostname + "'s password:")
    return password


def hostinfo(hostname):
    vars = {}
    vars['ansible_host'] = nc_inv[hostname]['ansible_host']
    vars['ansible_port'] = nc_inv[hostname]['ansible_port']
    vars['ansible_user'] = nc_inv[hostname]['ansible_user']
    vars['ansible_ssh_pass'] = get_srv_pass(hostname)
    return vars

def grouplist(groupname):
    srvs = {}
    srvs['_meta'] = {
        'hostvars':{}
    }

    srvs[groupname] = {
        'hosts' : []
    }
    for srv in nc_inv.keys():
        srvs[groupname]['hosts'].append(srv)
        vars = hostinfo(srv)
        srvs['_meta']['hostvars'][srv]=vars
    print json.dumps(srvs, indent=4)


if __name__ == "__main__":
    try: 
        grouplist('servers')
    except:
        Usage()
