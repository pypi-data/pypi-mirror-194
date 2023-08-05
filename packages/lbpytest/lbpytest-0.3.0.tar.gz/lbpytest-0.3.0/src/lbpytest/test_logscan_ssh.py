import sys

from .controlmaster import SSH
from .logscan import Logscan, InputStream


def test_basic_echo(host):
    ssh = SSH(host)
    p = ssh.Popen('echo zyx')
    l = Logscan({'n0': InputStream(p.stdout)}, timeout=1)
    l.event(['zyx'], filters={'n0': []}, verbose_out=sys.stdout)
    ssh.close()
