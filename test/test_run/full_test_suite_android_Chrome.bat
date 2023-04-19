Set envFile=AndroidChrome.json
Set language=English
Set thread=6
cd ../..
py.test --html="test/test_run/test_result" --env=%envFile% --language=%language% test\preparation\prepare_test_data.py
py.test --html="test/test_run/test_result" --env=%envFile% --language=%language% -v -m "not OnlyDesktop" test\testcases -n %thread%
pause