# lbpytest

[![PyPI](https://img.shields.io/pypi/v/lbpytest)](https://pypi.org/project/lbpytest/)

Utilities for Python-driven integration tests at LINBIT.

## Installation

```bash
pip install lbpytest
```

## Usage

### [ControlMaster](./src/lbpytest/controlmaster.py)

```python
from lbpytest.controlmaster import SSH
from io import StringIO
import subprocess
import sys

try:
    ssh = SSH("myhost.example.org")
except subprocess.CalledProcessError as e:
    print(e.stderr.decode('utf-8'), file=sys.stderr)
    raise e

# Run command using the hosts stdin/stdout/stderr
ssh.run("echo 'Hello, World!'")

# Save command output
output = StringIO()
ssh.run("echo 'Hello, World!'", stdout=output)
print(output.getvalue()) # prints Hello, World!

ssh.close()
```

### [Logscan](./src/lbpytest/logscan.py)

See [`test_logscan.py`](./src/lbpytest/test_logscan.py) and
[`test_logscan_ssh.py`](./src/lbpytest/test_logscan_ssh.py).

## Testing

The unit tests for this project can be run using `pytest`:

```
$ pytest src/lbpytest
```

Note that for the `ControlMaster` tests, a `--host` option is required. This should specify the IP address or hostname
of an SSH server to use for the test.

## Type Checking

This library uses [type annotations](https://docs.python.org/3/library/typing.html).
The [mypy](http://mypy-lang.org/) tool can be used to verify these annotations:

```
$ mypy src/lbpytest
```

## License

[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
