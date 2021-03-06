#!/usr/bin/env python
# Refer to from http://stackoverflow.com/questions/27590039/running-ansible-playbook-using-python-api
# 2017-02-17 Colynn Liu


import os
import sys
from collections import namedtuple

from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

# Callback
from ansible import constants as C
from lib.default import DefaultCallback
results_callback = DefaultCallback()

variable_manager = VariableManager()
loader = DataLoader()

inventory = Inventory(loader=loader, variable_manager=variable_manager,  host_list='lib/inventory-host.py')
playbook_path = 'site.yml'

if not os.path.exists(playbook_path):
    print '[INFO] The playbook does not exist'
    sys.exit()

Options = namedtuple('Options', ['listtags', 'listtasks', 'listhosts', 'syntax',
                                 'connection', 'module_path', 'forks', 'remote_user', 'private_key_file',
                                 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args',
                                 'become', 'become_method', 'become_user', 'verbosity', 'check']
                     )
# Refer to: ansible/playbook/play_context.py
# reset the remote_user back to the default if none was specified, to prevent
# the delegated host from inheriting the original host's setting 
# So, defined the default remote_user is None.

# when use paramiko connection plugin, theses args(ssh_extra_args, ssh_common_args, ssh_args) will be joined to a string.
# and default, ssh_args = C.ANSIBLE_SSH_ARGS,
# so if you want to use paramiko, you need change the defined of 'ssh_common_args','ssh_extra_args'. : ssh_common_args='', ssh_extra_args=''
# Refer to: plugins/connection/paramiko_ssh.py

options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                  module_path=None, forks=100, remote_user=None, private_key_file=None,
                  ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None,
                  become=False, become_method=None, become_user='root', verbosity=None, check=False
                  )

variable_manager.extra_vars = {'hosts': 'localhost', 'api_token': 'apixxxxxxx12333333', 'password': True}  # This can accomodate various other command line arguments.`

passwords = {}

# reset default stdout callback
C.DEFAULT_STDOUT_CALLBACK = results_callback

pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                        loader=loader, options=options, passwords=passwords)

results = pbex.run()
