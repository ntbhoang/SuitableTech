timeout 28800
cd "../.."
Set envFile=WindowsChrome.json
Set language=English
Set thread=6

py.test --html="test/test_run/test_result" --env=%envFile% --language=%language% test\preparation\prepare_test_data.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\full_site_admin_mode\device_group_admin\devices\devices_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\full_site_admin_mode\device_group_admin\devices_group_access\device_group_access_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\full_site_admin_mode\device_group_admin\users\users_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\full_site_admin_mode\device_group_admin\device_group_admin_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\simplified_site_admin_mode\device_admin\devices\devices_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\simplified_site_admin_mode\device_admin\users\user_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\admins\simplified_site_admin_mode\device_admin\device_admin_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\devices\full_site_admin_mode\devices_site_admin_mode_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\devices\simplified_site_admin_mode\simplied_site_admin_mode_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\groups_full_site_admin_mode_only\device_groups_full_site_admin_mode_only\device_groups_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\groups_full_site_admin_mode_only\devices_group_access_full_site_admin_mode_only\devices_group_access_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\groups_full_site_admin_mode_only\user_groups\user_group_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\infrastructure_email_messages\notify_users_admins\notify_users_admins_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\infrastructure_email_messages\notify_users_only\notify_user_only_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\invite_attract_url_functionality\email_admin_request_notifications\email_admin_request_notifications_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\invite_attract_url_functionality\settings\invite_attract_url_functionality_settings_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\local_run_only\related_to_native_window_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\users\full_site_admin_mode\add_users\authorization_social_network_user\authorization_social_network_user_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\users\full_site_admin_mode\add_users\suitable_user\suitable_user_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\users\full_site_admin_mode\remove_users\suitable_user\suitetable_user_test.py
py.test -n %thread% --html="test/test_run/test_result" --env=%envFile% --language=%language% test\testcases\users\simplified_site_admin_mode\non_admin_user_login_management_web_app_account_home_pg_view\non_admin_user_login_management_web_app_account_home_pg_view_test.py
pause