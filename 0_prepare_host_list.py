#!/usr/bin/env python
#

import sys

host_path = 'hosts'
print "[Info] Using '" + host_path + "' as inventory host file."

def check_host_tag(host_tag):
    f1 = open(host_path, 'r')
    items = f1.readlines()
    f1.close()
    for item in items:
        if item == '\n':
            continue
        if host_tag  == item.split()[0]:
            print "[Waring] this host_tag already added to hosts file."
            return True

while True:
    host_tag = raw_input("host purpose tag: ")
    host_tag = host_tag.strip()

    if check_host_tag(host_tag):
        continue
    if host_tag == "":
        continue
    host_ip = raw_input("host ip: ")
    host_port = raw_input("host port[default 22]: ")
    ssh_user = raw_input("host ssh user: ")
    
    host_ip = host_ip.strip()
    host_port = host_port.strip()
    ssh_user = ssh_user.strip()

    # default port 22
    if host_port == "":
        host_port = "22"

    host_item = host_tag + " ansible_host=" + host_ip +  " ansible_port=" + host_port + " ansible_user=" + ssh_user + "\n"
    f2 = open(host_path, 'a')
    f2.write(host_item)
    f2.flush()
    exit_status = raw_input("Add more host item[enter] or exit[q]:" )
    if exit_status ==  "q":
        break
f2.close()
