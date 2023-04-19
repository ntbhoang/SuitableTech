class EmptyDevicesGroupNameException(Exception):
    pass


class EmptyUserGroupNameException(Exception):
    pass


class DevicesGroupNotCreated(Exception):
    pass


class MissingArgumentException(Exception):
    def __init__(self, class_name, method_name, miss_arg_name):
        self.parameter = ("Missing argument {} in the method {}::{}()" % (class_name, method_name, miss_arg_name) )

    def __str__(self):
        return repr(self.parameter)


class FunctionNotSupportedException(Exception):
    def __init__(self, exception_message):
        self.message = exception_message

    def __str__(self):
        return repr(self.message)
    
    
class ElementIsNone(Exception):
    def __init__(self, driver, action, locator):
        self._driver = driver
        self._action = action
        self._locator = locator
        self._driver.save_screenshot()
        
    def __str__(self):
        return repr("{} failed. Element {} not found.".format(self._action, self._locator))



