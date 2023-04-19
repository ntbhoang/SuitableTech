
import re
from selenium.webdriver.common.by import By
from core.webdriver.elements.element_base import ElementBase
from datetime import datetime
from core.webdriver.elements.element import Element
from common.application_constants import ApplicationConst


class _DatePickerLocator(object):
    @staticmethod
    def _btnDay(int_day):
        return By.XPATH, "//table//tbody//button[@ng-click='select(dt.date)']//span[not(contains(@class, 'text-muted')) and .='%.2d']" % int_day

    @staticmethod
    def _btnMonth(month_name):
        return By.XPATH, u"//table//tbody//button[@ng-click='select(dt.date)']//span[.='%s']" % month_name

    @staticmethod
    def _btnYear(int_year):
        return By.XPATH, "//table//tbody//button[@ng-click='select(dt.date)']//span[.='%d']" % int_year
    
"""
Note that this class is picker from <ul> tag name
"""


class DatePicker(ElementBase):
    
    @property
    def _btnMovePrev(self):
        return Element(self._driver, By.XPATH, self._value + "//table//thead//button[@ng-click='move(-1)']")

    @property
    def _btnToggleMode(self):
        return Element(self._driver, By.XPATH, self._value + "//table//thead//button[@role='heading']")

    @property
    def _btnMoveNext(self):
        return Element(self._driver, By.XPATH, self._value + "//table//thead//button[@ng-click='move(1)']")

    @property
    def _btnToday(self):
        return Element(self._driver, By.XPATH, self._value + "//button[@ng-click=\"select('today', $event)\"]")

    @property
    def _btnClear(self):
        return Element(self._driver, By.XPATH, self._value + "//button[@ng-click='select(null, $event)']")

    @property
    def _btnClose(self):
        return Element(self._driver, By.XPATH, self._value + "//button[@ng-click='close($event)']")

    @property
    def _tblCalendar(self):
        return Element(self._driver, By.XPATH, self._value + "//table/..")
    
    def _btnDay(self, int_day):
        return Element(self._driver, *_DatePickerLocator._btnDay(int_day))

    def _btnMonth(self, month_name):
        return Element(self._driver, *_DatePickerLocator._btnMonth(month_name))

    def _btnYear(self, int_year):
        return Element(self._driver, *_DatePickerLocator._btnYear(int_year))
    
    """ Methods """
    def __init__(self, driver, by=By.XPATH, value=None):
        ElementBase.__init__(self, driver, by, value)
    
    def today(self):
        self._btnToday.click()

    def clear(self):
        self._btnClear.click()

    def close(self):
        self._btnClose.click()

    def select_day(self, int_day, int_month=None, int_year=None):
        """
        @summary: This action is used to select day
        @param int_day: day
        @param int_month: month
        @param int_year: year
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        self._go_to_day_selected_mode(int_month, int_year)
        self._btnDay(int_day).click_element()
        self.wait_until_disappeared(2)
        
    def _select_year(self, int_year):
        """
        @summary: This action is used to select year
        @param int_year: year
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        if int_year <= 0:
            raise ValueError
        self._go_to_year_selected_mode(int_year)
        self._btnYear(int_year).click_element()
        
    def _select_month(self, int_month, int_year=None):
        """
        @summary: This action is used to select month
        @param int_month: month
        @param int_year: year
        @author: Thanh Le
        @created_date: August 5, 2016
        """

        if int_month <= 0 or int_month > 12:
            raise ValueError
        self._go_to_month_selected_mode(int_year)

        key = "MON%.2d" % int_month
        month_as_text = ApplicationConst.get_date_time_label(key)

        if self._btnMonth(month_as_text).is_displayed(2):
            self._btnMonth(month_as_text).click_element()
        else:
            month_as_text = u"{}月".format(int_month)
            self._btnMonth(month_as_text).click_element()
        
    def _go_to_year_selected_mode(self, target_year):
        # go to month selected mode if need
        if self._is_day_selected_mode():
            self._btnToggleMode.click()

        # go to year selected mode if need
        if self._is_month_selected_mode():
            self._btnToggleMode.click()

        # find year target button
        toggle_mode_value = self._btnToggleMode.text
        years = [int(s) for s in re.findall(r'\b\d+\b', toggle_mode_value)]
        if years[0] <= target_year <= years[1]:
            return

        # go to previous year-block if needed
        while target_year < years[0]:
            self._btnMovePrev.click()
            toggle_mode_value = self._btnToggleMode.text
            years = [int(s) for s in re.findall(r'\b\d+\b', toggle_mode_value)]
            if years[0] <= target_year <= years[1]:
                return

        # go to next year-block if needed
        while target_year > years[1]:
            self._btnMoveNext.click()
            toggle_mode_value = self._btnToggleMode.text
            years = [int(s) for s in re.findall(r'\b\d+\b', toggle_mode_value)]
            if years[0] <= target_year <= years[1]:
                return
    
    def _go_to_month_selected_mode(self, target_year=None):
        if target_year:
            self._select_year(target_year)
            return
        
        # go to month selected mode if need
        if self._is_day_selected_mode():
            self._btnToggleMode.click()
        else:
            if self._is_year_selected_mode():
                # target_year is not defined, user current
                self._select_year(datetime.now().year)

    def _go_to_day_selected_mode(self, target_month=None, target_year=None):
        if target_month:
            self._select_month(target_month, target_year)
        else:
            self._select_month(datetime.now().month, None)
    
    def _is_year_selected_mode(self):
        return True if 'uib-yearpicker' in self._tblCalendar.get_attribute("class") else False
        
    def _is_month_selected_mode(self):
        return True if 'uib-monthpicker' in self._tblCalendar.get_attribute("class") else False
    
    def _is_day_selected_mode(self):
        return True if 'uib-daypicker' in self._tblCalendar.get_attribute("class") else False
