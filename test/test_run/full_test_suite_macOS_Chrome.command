
cd "$(dirname "$0")"/../..

/Library/Frameworks/Python.framework/Versions/3.5/bin/py.test --html="test/test_run/test_result" --env=MacChrome.json --language=English test/preparation/prepare_test_data.py

/Library/Frameworks/Python.framework/Versions/3.5/bin/py.test --html="test/test_run/test_result" --env=MacChrome.json --language=English -v -m "not OnlyMobile" test/testcases