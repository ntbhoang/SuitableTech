import os
import pytest
from data_test import setting
import json
import threading

RLOCK = threading.RLock()

def pytest_addoption(parser):
    parser.addoption("--env", action = "store", default = 'WindowsIE.json', help = "The environment where the test should run")
    parser.addoption("--language", action = "store", default = 'English', help = "Language of Application Under Test")


@pytest.fixture(autouse = True)
def collect_information(request):
    with RLOCK:
        run_info = {"language": "ENGLISH","environmentFile": "WindowsChrome.json"}
        
        env = request.config.getoption('--env')
        language = request.config.getoption('--language')
            
        run_info["environmentFile"] = env
        run_info["language"] = language.upper()
        
        file_path = os.path.dirname(setting.__file__)
        write_file = open(file_path + os.path.sep + "ExecutionSettings.json", "w")
        write_file.write(json.dumps(run_info))
        write_file.close()


