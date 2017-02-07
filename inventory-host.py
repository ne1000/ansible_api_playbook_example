#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import os
import sys
import getpass
from commands import getoutput

# INV_PATH = os.getenv('NC_HOST_FILE')
# INV_PATH = "/tmp/hosts"

try:
    import json
except ImportError:
    import simplejson as json

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

# nc_inv = OrderedDict() 
nc_inv = {'colynn-test1': {'ansible_ssh_host': '172.31.16.142', 'ansible_ssh_port': '22'}}


def Usage():
    print "Usage:  %s --list" % sys.argv[0]
    sys.exit(1)

def get_srv_pass(hostname):
    """
    ncadmin@srv-name's password:
    """
    password = getpass.getpass("ncadmin@" + hostname + "'s password:")
    return password


def hostinfo(hostname):
    vars = {}
    vars['ansible_ssh_host'] = nc_inv[hostname]['ansible_ssh_host']
    vars['ansible_ssh_port'] = nc_inv[hostname]['ansible_ssh_port']
    vars['ansible_ssh_user'] = 'ncadmin'
    vars['ansible_ssh_pass'] = get_srv_pass(hostname)
    return vars
    #print json.dumps(vars, indent=4)

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
    #ldap_hosts = parse_inv(INV_PATH)
    #if ldap_hosts > 0:
    #   ldap_user = getpass.getuser()
    #   ldap_pw = getpass.getpass(ldap_user + "@servers ldap's password: ")

    try: 
        grouplist('servers')
    except:
        Usage()

