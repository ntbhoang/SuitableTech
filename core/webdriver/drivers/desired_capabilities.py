class BrowserStackDesiredCapabilities(object):
    """
    Set of default supported desired capabilities of BrowserStack.

    Note: Always use '.copy()' on the DesiredCapabilities object to avoid the side
    effects of altering the Global class instance.

    """

    FIREFOX = {
        'browser': 'Firefox',
        'browser_version': '49.0',
        'os': 'Windows',
        'os_version': '7',
        'resolution': '1280x1024'
    }

    INTERNETEXPLORER = {
        'browser': 'IE',
        'browser_version': '11.0',
        'os': 'Windows',
        'os_version': '7',
        'resolution': '1280x1024',
        'browserstack.ie.enablePopups': True
    }

    EDGE = {
        'browser': 'Edge',
        'browser_version': '14.0',
        'os': 'Windows',
        'os_version': '10',
        'resolution': '1280x1024'
    }

    CHROME = {
        'browser': 'Chrome',
        'browser_version': '54.0',
        'os': 'Windows',
        'os_version': '7',
        'resolution': '1280x1024'
    }

    SAFARI = {
        'browser': 'Safari',
        'browser_version': '10.0',
        'os': 'OS X',
        'os_version': 'Sierra',
        'resolution': '1280x1024',
        'browserstack.safari.enablePopups': True
    }


class SauceLabsDesiredCapabilities(object):
    """
    Set of default supported desired capabilities of SauceLabs.

    Note: Always use '.copy()' on the DesiredCapabilities object to avoid the side
    effects of altering the Global class instance.

    """

    FIREFOX = {
        'browserName': 'firefox',
        'version': '49.0',
        'platform': 'Windows 7',
        'screenResolution': '1600x1200',
        'recordVideo': True,
        'recordScreenshots': False
    }

    INTERNETEXPLORER = {
        'browserName': 'internet explorer',
        'version': '11.0',
        'platform': 'Windows 7',
        'screenResolution': '1600x1200',
        'recordVideo': True,
        'recordScreenshots': False
    }

    EDGE = {
        'browserName': 'microsoftedge',
        'browser_version': '14',
        'platform': 'Windows 7',
        'screenResolution': '1600x1200',
        'recordVideo': True,
        'recordScreenshots': False
    }

    CHROME = {
        'browserName': 'chrome',
        'version': '54.0',
        'platform': 'Windows 7',
        'screenResolution': '1600x1200',
        'recordVideo': False,
        'recordScreenshots': False
    }

    SAFARI = {
        'browserName': 'safari',
        'version': '10.0',
        'platform': 'OS X 10.12',
        'screenResolution': '1600x1200',
        'recordVideo': True,
        'recordScreenshots': False
    }

