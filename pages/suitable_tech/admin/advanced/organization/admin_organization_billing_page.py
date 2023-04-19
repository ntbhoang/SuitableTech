from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from common.application_constants import ApplicationConst
from pages.suitable_tech.admin.advanced.organization.admin_organization_common_page import OrganizationCommonPage
from common.constant import Constant


class _OrganizationBillingPageLocator(object):
    _btnChangeCreditCard = (By.CSS_SELECTOR, "button[ng-click='openCreditCardModal()']")
    _lblBrand = (By.CSS_SELECTOR, "span[ng-show='card.card_brand']")
    _lblExpiration = (By.CSS_SELECTOR,"span[ng-class='{\"icon-error\": expiredCard}']")

    @staticmethod
    def _lblName(label_name):
        return (By.XPATH,u"//div[.='{}']/..//div[contains(@class,'card-details ng-binding')]".format(label_name))
    @staticmethod
    def _icnBrand(brand):
        return (By.CSS_SELECTOR, u"span[brand='card.card_brand'] i[ng-show='brand == \"{}\"']".format(brand))
    
    
class OrganizationBillingPage(OrganizationCommonPage):
    """
    @description: This is page object class for Admin Organization Authentication page.
        This page will be opened after clicking Billing tab on Organization page.
        Please visit https://stg1.suitabletech.com/manage/129/#/organization/billing/ for more details.
    @page: Admin Organization Billing page
    @author: thanh.viet.le
    """

    """    Properties    """
    @property
    def _btnChangeCreditCard(self):
        return Element(self._driver, *_OrganizationBillingPageLocator._btnChangeCreditCard)
    @property
    def _lblBrand(self):
        return Element(self._driver, *_OrganizationBillingPageLocator._lblBrand)
    @property
    def _lblExpiration(self):
        return Element(self._driver, *_OrganizationBillingPageLocator._lblExpiration)

    def _lblName(self,label_name):
        return Element(self._driver, *_OrganizationBillingPageLocator._lblName(label_name))
    def _icnBrand(self, brand):
        return Element(self._driver, *_OrganizationBillingPageLocator._icnBrand(brand))

    """    Methods    """
    def __init__(self, driver):  
        """      
        @summary: Constructor method    
        @param driver: Web driver 
        @author: Khoi Ngo       
        """      
        OrganizationCommonPage.__init__(self, driver)


    def open_change_card_details_dialog(self):
        """
        @summary: The method to open change card details dialog
        @return: ChangeCardDetailsDialog
        @author: Khoi Ngo
        """
        self._btnChangeCreditCard.click()
        from pages.suitable_tech.admin.dialogs.change_card_details_dialog import ChangeCardDetailsDialog
        ChangeCardDetailsDialog(self._driver)._dialog.wait_until_displayed(3)
        return ChangeCardDetailsDialog(self._driver)


    def is_new_credit_card_details_shown_up(self, number, name, exp_month, exp_year):
        """
        @summary:  Check if new credit card details is shown up on the main page or not
        @author: Khoi Ngo
        """
        if number == Constant.AmericanExpress['number']:
            brand = Constant.AmericanExpress['brand']
        else:
            brand = Constant.Discover['brand']

        if "ng-hide" in self._icnBrand(brand).get_attribute("class"):
            return False
        if brand not in self._lblBrand.text:
            return False
        if self._lblExpiration.text != (exp_month+"/"+exp_year):
            return False
        if self._lblName(ApplicationConst.LBL_NAME_ON_CARD).text != name:
            return False
        return True

