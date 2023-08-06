import pytest
from src._internal import Launch, Data

def pytest_addoption(parser):
    parser.addoption("--report", action="store", default=None,
                     help="path to the script to be executed before running tests")

def pytest_runtestloop(session):
    script_path = session.config.getoption("--report")
    if script_path:
        Data.parse()
        Launch.start_launch()

def pytest_sessionfinish(session, exitstatus):
    script_path = session.config.getoption("--report")
    if script_path:
        Launch.finish_launch()