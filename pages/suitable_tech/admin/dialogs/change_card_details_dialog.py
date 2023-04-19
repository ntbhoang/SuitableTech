from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from pages.suitable_tech.admin.dialogs.dialog_base import DialogBase
from pages.suitable_tech.admin.advanced.organization.admin_organization_setting_page import OrganizationSettingsPage


class _ChangeCardDetailsDlgLocator(object):
    _txtNumber = (By.CSS_SELECTOR,".modal-content input[ng-model='card.card_number']")
    _txtName = (By.CSS_SELECTOR,".modal-content input[ng-model='card.card_name']")
    _txtExpMonth = (By.CSS_SELECTOR,".modal-content input[ng-model='card.card_exp_month']")
    _txtExpYear = (By.CSS_SELECTOR,".modal-content input[ng-model='card.card_exp_year']")
    _txtSecurityCode = (By.CSS_SELECTOR,".modal-content input[ng-model='card.cvc']")
    _btnUpdateCard = (By.CSS_SELECTOR,".modal-content button[ng-click='updateCard()']")

class ChangeCardDetailsDialog(DialogBase):
    """
    @description: This Page Object is used for Change Card Details Dialog.
    This dialog appear when user want to change credit card
    @page: Change Card Details Dialog

    """

    """    Properties    """
    @property
    def _txtNumber(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._txtNumber)
    @property
    def _txtName(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._txtName)
    @property
    def _txtExpMonth(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._txtExpMonth)
    @property
    def _txtExpYear(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._txtExpYear)
    @property
    def _txtSecurityCode(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._txtSecurityCode)
    @property
    def _btnUpdateCard(self):
        return Element(self._driver, *_ChangeCardDetailsDlgLocator._btnUpdateCard)


    """    Methods    """
    def __init__(self, driver):
        """
        @summary: Constructor method
        @param driver: Web Driver
        @author: Thanh Le
        """
        DialogBase.__init__(self, driver)


    def fill_credit_card_info(self, number="", name="", exp_month="", exp_year="", security_code=""):
        """
        @summary: This action is used to fill credit card detail
        @param: number: new number would like to set for credit card
        @param: name: new name would like to set for credit card
        @param: exp_month: expiration month
        @param: exp_year: expiration year
        @param: security_code: security code is set for credit card
        @return: ChangeCardDetailsDialog
        @author: Thanh Le
        """
        if number:
            self._txtNumber.type(number)
        if name:
            self._txtName.type(name)
        if exp_month:
            self._txtExpMonth.type(exp_month)
        if exp_year:
            self._txtExpYear.type(exp_year)
        if security_code:
            self._txtSecurityCode.type(security_code)
        return self


    def update_credit_card(self, cancel=False):
        """
        @summary: This action is used to decide updating credit card detail or not
        @param: cancel: cancel update or not
        @return: OrganizationSettingsPage
        @author: Thanh Le
        """
        if cancel:
            self._btnCancel.wait_until_clickable().click()
        else:
            self._btnUpdateCard.wait_until_clickable().click()
        return OrganizationSettingsPage(self._driver)


    def clear_all_update_credit_card_info(self):
        """
        @summary: This action is used to decide updating credit card detail or not
        @param: cancel: cancel update or not
        @return: OrganizationSettingsPage
        @author: Thanh Le
        """
        self._txtNumber.clear()
        self._txtName.clear()
        self._txtExpMonth.clear()
        self._txtExpYear.clear()
        self._txtSecurityCode.clear()
        return self

