#! /usr/bin/env python
from io import StringIO

import fcntl
import os
import pytest
import sys

from .logscan import Logscan, NegativeMatchException, TimeoutException, InputStream

one = '''xyz

def
abc

def
abc'''

two = '''abc t:0
def

abc t:1
def

zyx'''

three = '''a:0 b:1 c:1
a:1 b:1 c:0
a:1 b:0 c:1
bad
a:1 b:1 c:1'''


class FDString:
    """
    Make a string available as a file descriptor. This is useful for supplying
    data to functions that expect an actual file descriptor rather than any
    file-like object. For instance, "Logscan.event()", which uses
    "select.select".
    """

    def __init__(self, text: str, close_write: bool = True) -> None:
        self.text = text
        self.close_write = close_write
        self.read_fd = -1
        self.write_fd = -1

    def __enter__(self):
        read_fd, write_fd = os.pipe()
        self.read_fd = read_fd
        os.write(write_fd, self.text.encode('utf-8'))
        if self.close_write:
            os.close(write_fd)
        else:
            self.write_fd = write_fd

        fl = fcntl.fcntl(read_fd, fcntl.F_GETFL)
        fcntl.fcntl(read_fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

        # Convert numeric file descriptor into file-like object
        return os.fdopen(read_fd, "rb")

    def __exit__(self, type, value, traceback):
        if self.write_fd != -1:
            os.close(self.write_fd)
        os.close(self.read_fd)


def test_match():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        l.event(['zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)


def test_match_no():
    with FDString(one) as fd_one:
        l = Logscan({'one': InputStream(fd_one)}, timeout=2)
        with pytest.raises(NegativeMatchException):
            l.event(['abc', 'def'], no=['xyz', 'zyx'], filters={'one': [[]]}, verbose_out=sys.stdout)


def test_match_always_no():
    with FDString(one) as fd_one:
        l = Logscan({'one': InputStream(fd_one)}, timeout=2)
        with pytest.raises(NegativeMatchException):
            l.event(['abc', 'def'], always_no=['xyz', 'zyx'], filters={'one': [[]]}, verbose_out=sys.stdout)


def test_match_not_no():
    with FDString(one) as fd_one:
        l = Logscan({'one': InputStream(fd_one)}, timeout=2)
        with pytest.raises(EOFError):
            l.event(['not_in_input'], no=['zyx'], filters={'one': [[]]}, verbose_out=sys.stdout)


# logscan -y abc -y def -n xyz -n zyx two
def test_not_match_no_skipped():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        l.event(['abc', 'def'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)


# logscan --verbose -y a.c -y d.f -n xyz -n zyx two
def test_not_match_no_skipped_regex():
    tee = StringIO()
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two, tee_out=tee)}, timeout=2)
        l.event(['a.c', 'd.f'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)
    # The string written to "tee" may include more than the amount needed for the match.
    assert tee.getvalue().startswith('\n'.join(two.splitlines()[:5]))


def test_not_match_no_skipped_multiple():
    # test that lines are not dropped when calling event multiple times
    tee = StringIO()
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two, tee_out=tee)}, timeout=2)
        l.event(['a.c'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)
        l.event(['d.f'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)
        l.event(['a.c'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)
        l.event(['d.f'], no=['xyz', 'zyx'], filters={'two': [[]]}, verbose_out=sys.stdout)
    assert tee.getvalue().startswith('\n'.join(two.splitlines()[:5]))


def test_no_input():
    with FDString('') as fd_empty:
        l = Logscan({'empty': InputStream(fd_empty)}, timeout=2)
        with pytest.raises(EOFError):
            l.event(['abc'], filters={'empty': [[]]}, verbose_out=sys.stdout)


def test_multiple_inputs():
    with FDString(one) as fd_one, FDString(two) as fd_two:
        l = Logscan({'one': InputStream(fd_one), 'two': InputStream(fd_two)}, timeout=2)
        # abc should match in both
        l.event(['abc'], filters={'one': [[]], 'two': [[]]}, verbose_out=sys.stdout)
        with pytest.raises(EOFError):
            # xyz is only in one stream, so it should not match
            l.event(['xyz'], filters={'one': [[]], 'two': [[]]}, verbose_out=sys.stdout)


def test_multiple_inputs_short():
    with FDString('zyx') as fd_short, FDString(two) as fd_two:
        l = Logscan({'short': InputStream(fd_short), 'two': InputStream(fd_two)}, timeout=2)
        # zyx should match in both
        l.event(['zyx'], filters={'short': [[]], 'two': [[]]}, verbose_out=sys.stdout)


def test_filter_match():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        l.event(['abc'], filters={'two': [['t:1']]}, verbose_out=sys.stdout)


def test_filter_match_no():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        with pytest.raises(EOFError):
            # All matches are filtered out, so it should not match
            l.event(['abc'], filters={'two': [['t:5']]}, verbose_out=sys.stdout)


def test_filter_exclude_no():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        # The "no" regex would match, but is filtered out
        l.event(['abc t:1'], no=['def'], filters={'two': [['t:.*']]}, verbose_out=sys.stdout)


def test_filter_multiple_same_line():
    with FDString(three) as fd_three:
        l = Logscan({'three': InputStream(fd_three)}, timeout=2)
        l.event(['a:1'], filters={'three': [['b:1', 'c:1']]}, verbose_out=sys.stdout)


def test_filter_multiple_same_line_no():
    with FDString(three) as fd_three:
        l = Logscan({'three': InputStream(fd_three)}, timeout=2)
        with pytest.raises(NegativeMatchException):
            l.event(['a:1'], always_no=['bad'],
                    filters={'three': [['b:1', 'c:1']]}, verbose_out=sys.stdout)


def test_filter_multiple_different_line():
    with FDString(three) as fd_three:
        l = Logscan({'three': InputStream(fd_three)}, timeout=2)
        l.event(['a:1'], always_no=['bad'],
                filters={'three': [['b:1'], ['c:1']]}, verbose_out=sys.stdout)


def test_match_capture():
    with FDString(two) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=2)
        l.event(['def'], filters={'two': [[]]}, verbose_out=sys.stdout)
        matches = l.event(['abc t:([0-9]*)'], filters={'two': [[]]}, verbose_out=sys.stdout)
        assert matches == [('1',)]


def test_timeout():
    with FDString(two, close_write=False) as fd_two:
        l = Logscan({'two': InputStream(fd_two)}, timeout=1)
        with pytest.raises(TimeoutException):
            l.event(['not_in_input'], filters={'two': [[]]}, verbose_out=sys.stdout)
