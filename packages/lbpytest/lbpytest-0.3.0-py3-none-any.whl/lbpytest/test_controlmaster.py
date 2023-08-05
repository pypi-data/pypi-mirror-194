#! /usr/bin/env python

from .controlmaster import SSH, TimeoutException
from io import StringIO
import re
import subprocess
import pytest

def test_basic_echo(host):
    ssh = SSH(host)
    output = StringIO()
    ret = ssh.run('echo -n test', stdout=output)
    ssh.close()
    assert ret == 0
    assert output.getvalue() == 'test'

def test_return_code(host):
    ssh = SSH(host)
    ret = ssh.run('exit 27')
    ssh.close()
    assert ret == 27

def test_long_echo(host):
    ssh = SSH(host)
    output = StringIO()
    expect='A'*1000000
    ret = ssh.run("""bash -c 'printf "A%.0s" {1..1000000}'""", stdout=output)
    ssh.close()
    assert ret == 0
    assert len(output.getvalue()) == len(expect)
    assert output.getvalue() == expect

def test_many_lines(host):
    ssh = SSH(host)
    output = StringIO()
    expect='A\n'*100000
    ret = ssh.run("""bash -c 'for i in {1..100000}; do echo A; done'""", stdout=output)
    ssh.close()
    assert ret == 0
    assert len(output.getvalue()) == len(expect)
    assert output.getvalue() == expect

def test_split_utf8(host):
    ssh = SSH(host)
    output = StringIO()
    ret = ssh.run("""bash -c 'printf "\\xf0\\x9f" ; sleep 1 ; printf "\\x98\\x80"'""", stdout=output)
    print(output.getvalue())
    ssh.close()
    assert ret == 0
    assert len(output.getvalue()) == 1

def test_stdin(host):
    ssh = SSH(host)
    output = StringIO()
    expect='A\n'*1000
    stdin=StringIO(expect)
    ret = ssh.run('cat', stdin=stdin, stdout=output)
    assert ret == 0
    assert len(output.getvalue()) == len(expect)
    assert output.getvalue() == expect
    ssh.close()

def test_timeout_global(host):
    ssh = SSH(host, timeout=1)
    ssh.run('sleep 0')
    with pytest.raises(TimeoutException):
        ssh.run('sleep 2')
    ssh.close()

def test_timeout_run(host):
    ssh = SSH(host)
    ssh.run('sleep 1', timeout=2)
    with pytest.raises(TimeoutException):
        ssh.run('sleep 2', timeout=1)
    ssh.close()

def test_timeout_overrides(host):
    ssh = SSH(host, timeout=1)
    ssh.run('sleep 2', timeout=10)
    ssh.close()

def test_env(host):
    ssh = SSH(host)
    output = StringIO()
    expect = 'test'
    ret = ssh.run('echo -n $TEST', env={'TEST': expect}, stdout=output)
    ssh.close()
    assert ret == 0
    assert output.getvalue() == expect

def test_init_stderr():
    with pytest.raises(subprocess.CalledProcessError) as excinfo:
        SSH('server.invalid')
    # Expect some information about the invalid hostname
    expected_re = r'\bhostname\b'
    assert re.search(expected_re, excinfo.value.stderr.decode('utf-8')) is not None
