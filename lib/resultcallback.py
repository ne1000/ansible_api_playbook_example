## ResultCallback
from ansible.plugins.callback import CallbackBase
import json
import time

def show_process(task, host):
    # path = os.environ['STDOUT_PROCESS']       
    path = '/tmp/ansible_api_show_process.txt'
    fd = open(path, "a")
    fd.write("[" + host + "]: " + task + "\n")
    fd.close()

class ResultCallback(CallbackBase):
    """A sample callback plugin used for performing an action as results come in

    If you want to collect all results into a single object for processing at
    the end of the execution, look into utilizing the ``json`` callback plugin
    or writing your own custom callback plugin
    """
    TIME_FORMAT="%Y-%m-%d %H:%M:%S"
    MSG_FORMAT="\n%(host)s\n%(data)s"

    def log(self, host, category, data):
        # path = os.environ['STDOUT_FILE']       
        path = '/tmp/ansible_api_log_play.txt'
        now = time.strftime(self.TIME_FORMAT, time.localtime())
        fd = open(path, "a")
        fd.write(data)
        #if type(data) == dict:
        #    if 'verbose_override' in data:
        #        # avoid logging extraneous data from facts
        #        data = 'omitted'
        #    else:
        #        data = data.copy()
        #        fd.write(data)

                # if 'stdout' in data.keys():
                #    data= data['stdout']
                #    fd.write(data)
                # else:
                #    return False
        fd.close()

    def _new_task(self, task):
        return {
            'task': {
                'name': task.name,
                'id': str(task._uuid)
            },
            'hosts': {}
        }

    def playbook_on_task_start(self, task, is_conditional):
        # play = getattr(self, 'play', None)
        # print task
        # print self._new_task(task)
        # for host  in play._play_hosts:
        # show_process(task, self.host)
        pass

    def runner_on_failed(self, host, res, ignore_errors=False):
        self.log(host, 'FAILED', res)

    def runner_on_ok(self, host, res):
        self.log(host, 'OK', res)

    def runner_on_skipped(self, host, item=None):
        self.log(host, 'SKIPPED', '...')

    def runner_on_unreachable(self, host, res):
        self.log(host, 'UNREACHABLE', res)

    def runner_on_async_failed(self, host, res, jid):
        self.log(host, 'ASYNC_FAILED', res)

    def playbook_on_import_for_host(self, host, imported_file):
        self.log(host, 'IMPORTED', imported_file)

    def playbook_on_not_import_for_host(self, host, missing_file):
        self.log(host, 'NOTIMPORTED', missing_file)

