import fcntl
import os
import re
import sys
import subprocess
import select
import time
import uuid

from .incremental_line_split import IncrementalLineSplitter

class TimeoutException(Exception):
    pass

class SSH:
    """
    Class SSH serves as a wrapper for ssh ControlMaster connections. It manages
    exactly one connection and its corresponding ControlMaster socket.
    """

    def __init__(self, host, user='root', basedir='/tmp', timeout=None, connection_timeout=None):
        """
        The constructor immediately connects to a remote host and stores the
        ControlMaster socket in the local file system.

        :param host: the IP address or hostname of the host to connect to
        :param user: the username to log in as; defaults to 'root'
        :param basedir: the base directory where the ControlMaster socket will
            be stored; defaults to 'tmp'. The format of the file name is
            'controlmaster-$host', where $host is the host parameter
        :param timeout: the default timeout for subsequent calls to ``run()``
        :param connection_timeout: the timeout for the connection attempt;
            defaults to ``timeout``
        :raises subprocess.CalledProcessError: When the ssh connection cannot
            be established. The exception contains the captured stdout and
            stderr from the ssh command.
        """
        self.user = user
        self.host = host
        self.sockpath = os.path.join(basedir, 'controlmaster-'+self.host+'-'+uuid.uuid4().hex)
        self.timeout = timeout

        # With the combination of flags below, older versions of ssh fail to
        # close stderr. This was fixed in release 8.5 by
        # https://github.com/openssh/openssh-portable/commit/396d32f3a1a16e54df2a76b2a9b237868580dcbe
        # Verify that we are not using a broken version.
        p = subprocess.run(['ssh', '-V'], check=True, capture_output=True)
        output = p.stderr.decode('utf-8').strip()

        version_match = re.search(r'([0-9]+)\.([0-9]+)', output)
        if not version_match:
            raise RuntimeError("failed to find ssh version in: '{}'".format(output))

        major = int(version_match.group(1))
        minor = int(version_match.group(2))
        if major < 8 or (major == 8 and minor < 5):
            raise RuntimeError("unsupported ssh version: '{}'".format(output))

        subprocess.run(['ssh', '-S', self.sockpath, '-l', self.user,
                '-f', # Requests ssh to go to background just before command execution.
                '-N', # Do not execute a remote command.
                '-M', # Places the ssh client into "master" mode for connection sharing.
                self.host],
            check=True,
            capture_output=True,
            timeout=timeout if connection_timeout is None else connection_timeout)

    def close(self):
        """
        Close the ssh ControlMaster connection managed by this instance. If the
        connection is already closed, this is a no-op.
        """
        try:
            subprocess.run(['ssh', '-S', self.sockpath, '-O', 'exit', '_'],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            if e.returncode == 255:
                # socket not found, so it is probably already closed
                pass

    @staticmethod
    def inline_env(cmd, env):
        """
        Prepend environment variables to a command string.
        :param cmd: the original command string
        :param env: a dictionary containing the environment variables to be set
        :returns: a new command string that contains extra statements to export
            the environment variables before calling the command
        """
        parameters = " ".join(
            ["{}={}".format(k, v) for k, v in sorted(env.items())]
        )
        # NOTE: we actually need to use "export" here,
        # "{} {}".format(parameters, cmd) is not enough. This is because with
        # nontrivial shell statements like "command1 && command2", only command1
        # would actually have the variables set, but not command2.
        return "export {} && {}".format(parameters, cmd)

    def run(self, cmd_string, stdin=False, stdout=None, stderr=None, env=None, timeout=None):
        """
        Execute a command over the ssh ControlMaster connection. The user is
        responsible for making sure that the ControlMaster connection is open
        before calling this function.

        :param cmd_string: the command to execute. This function does no further
            quoting or escaping to this string
        :param stdin: a file-like object that the process's standard input should
            be read from. This is expected to produce only UTF-8 encoded data.
            The special value "None" means that the parent process's standard
            input will be used. The special value "False" means that no standard
            input is needed; the process's stdin will be closed immediately
        :param stdout: a file-like object that the process's standard output stream
            should be written to. The called process is expected to produce only
            UTF-8 encoded data. The special value "None" means that the parent
            process's standard output will be used
        :param stderr: a file-like object that the process's standard error stream
            should be written to. The called process is expected to produce only
            UTF-8 encoded data. The special value "None" means that the parent
            process's standard error will be used
        :param env: a dictionary containing extra environment variables to be
            set before the command is executed. This function "inlines" the
            environment variables in the command string
        :returns: the called process's exit code, once it exits
        """
        p = self.Popen(cmd_string, env)

        self.pipeIO(p, stdin, stdout, stderr, timeout=self.timeout if timeout is None else timeout)

        return p.wait()

    def Popen(self, cmd_string, env=None):
        """
        Low-level interface to start a process over the ssh ControlMaster
        connection.
        """
        if env:
            cmd_string = self.inline_env(cmd_string, env)

        p = subprocess.Popen(['ssh', '-S', self.sockpath, '_', cmd_string],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

        # make the output streams non-blocking so that we can read all
        # available bytes after 'select'
        self._set_nonblock(p.stdout)
        self._set_nonblock(p.stderr)

        return p

    def _set_nonblock(self, stream):
        fd = stream.fileno()
        fl = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

    def pipeIO(self, p, stdin=False, stdout=None, stderr=None, timeout=None):
        """
        Low-level interface to read/write standard streams of the process p
        to/from the file objects stdin, stdout and stderr.
        """
        stdout = stdout or sys.stdout
        stderr = stderr or sys.stderr
        if stdin is None:
            stdin = sys.stdin

        dest = { p.stdout: (IncrementalLineSplitter(), stdout),
                p.stderr: (IncrementalLineSplitter(), stderr) }
        read_list = [p.stdout, p.stderr]

        start_time = time.time()

        if stdin:
            p.stdin.write(stdin.read().encode('utf-8'))
        p.stdin.close()

        def check_io():
            ready_to_read = select.select(read_list, [], [], 1)[0]
            for stream in ready_to_read:
                splitter, out = dest[stream]
                # for non-blocking streams 'read()' just reads the available bytes
                data = stream.read()
                if data:
                    for line_bytes in splitter.split(data):
                        out.write(line_bytes.decode('utf-8') + '\n')
                else:
                    # end of file
                    read_list.remove(stream)

        while read_list:
            if timeout and time.time() - start_time >= timeout:
                raise TimeoutException()
            check_io()

        # Write any remaining data in case the output did not terminate with a
        # line break.
        for splitter, out in dest.values():
            out.write(splitter.read_remaining().decode('utf-8'))
