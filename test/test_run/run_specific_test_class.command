cd "`dirname "$0"`../.."
/Library/Frameworks/Python.framework/Versions/3.5/bin/py.test --html="test/test_run/test_result" --runenv=MacChrome.txt test/testcases/admins/full_site_admin_mode/device_group_admin/devices/devices_test.py