cd "../.."
Set envFile=WindowsEdge.json
Set language=English
Set thread=1

py.test --html="test/test_run/test_result" --env=%envFile% --language=%language% test\preparation\prepare_test_data.py
py.test --html="test/test_run/test_result" --env=%envFile% --language=%language% -v -m "not OnlyMobile" test\testcases -n %thread%
pause