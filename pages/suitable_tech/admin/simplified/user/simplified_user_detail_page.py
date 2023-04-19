from selenium.webdriver.common.by import By
from core.webdriver.elements.element import Element
from common.constant import Platform
from pages.suitable_tech.admin.advanced.beams.admin_beams_common_page import AdminBeamsCommonPage

class _SimplifiedUserDetailPageLocator(object):

    _btnDeleteUser = (By.XPATH, "//button[@ng-click='delete()' and @class='btn btn-danger pull-right hidden-xs']")
    _btnResendInvitation = (By.CSS_SELECTOR, "button[ng-click='resendInvitation()']")
    
    '''Mobile UI'''
    _btnMDeleteUser = (By.XPATH, "//button[@ng-click='delete()' and @class='btn btn-danger visible-xs']")

class SimplifiedUserDetailPage(AdminBeamsCommonPage):
    """
    @description: This is page object class for Simplified User Detail page.
        This page will be opened after clicking Users link.
    @page: Simplified User Detail page
    @author: Thanh Le
    """


    """    Properties    """
    @property
    def _btnDeleteUser(self):
        return Element(self._driver, *_SimplifiedUserDetailPageLocator._btnDeleteUser)
    
    @property
    def _btnMDeleteUser(self):
        return Element(self._driver, *_SimplifiedUserDetailPageLocator._btnMDeleteUser)
    
    @property
    def _btnResendInvitation(self):
        return Element(self._driver, *_SimplifiedUserDetailPageLocator._btnResendInvitation)
    
    """    Methods    """
    def __init__(self, driver):      
        """      
        @summary: Constructor method
        @param driver: Web driver 
        @author: Thanh Le   
        @created_date: May 16, 2017       
        """  
        AdminBeamsCommonPage.__init__(self, driver)
        self.wait_for_loading()
        
        
    def remove_this_user(self):
        """      
        @summary: This action is used to remove the user
        @return: SimplifiedDashboardPage
        @author: Thanh Le
        @created_date: 5/16/2017
        """
            
        if self._driver._driverSetting.platform == Platform.ANDROID or self._driver._driverSetting.platform == Platform.IOS:
            self._btnMDeleteUser.wait_until_clickable().click()
        else:
            self._btnDeleteUser.wait_until_clickable().click()
            
        from pages.suitable_tech.admin.dialogs.confirm_action_dialog import ConfirmActionDialog
        ConfirmActionDialog(self._driver).continue_dialog()
        
        from pages.suitable_tech.admin.simplified.dashboard.simplified_dashboard_page import SimplifiedDashboardPage 
        return SimplifiedDashboardPage(self._driver, False)
    
    
    def get_user_image_link(self):
        return AdminBeamsCommonPage.get_icon_link(self)


    def resend_invitation(self):
        """
        @summary: re-send invitation
        @return: AdminUserDetailPage
        @author: Khoi Ngo
        @created_date: October 12, 2017
        """
        self._btnResendInvitation.wait_until_clickable().click()
        return self


    def is_delete_user_button_display(self):
        """
        @summary: Check if the Delete This User button displays or not
        @return: True: the Delete This User displays, False: the Delete This User button does not display
        @author: Khoi Ngo
        """
        return self._btnDeleteUser.is_displayed()

