#! /usr/bin/env python

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default="127.0.0.1")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".
    option_value = metafunc.config.option.host
    if 'host' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize('host', [option_value])
