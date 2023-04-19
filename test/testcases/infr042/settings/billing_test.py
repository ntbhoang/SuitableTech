from test.testbase import TestBase
from pages.suitable_tech.user.login_page import LoginPage
from common.constant import Constant


class Billing(TestBase):

    def c33073_change_credit_card_details(self):
        """
        @author: Quang.Tran
        @date: 9/26/2017
        @summary: Verify welcome to beam block content
        @precondition:
            - Must have an admin who is also a purchasing admin in the organization.
            - Must have a credit card on file.

        @steps:
            1) Login to Suitabletech.com as an admin and
                select the organization settings via either the cog in simple mode,
                or the Organization primary-tab from in advanced mode
            2) Click the Billing tab in the sub menu
            3) Click the Update Credit Card button. The Change Card Details modal will appear
            4) Enter one of the following credit card numbers
                371449635398431 (American Express)
                6011111111111117 (Discover)
            5) Enter anything in the name column
            6) Enter a valid expiration month and year
            7) Enter any 4 digits for the security code
            8) Press Update Card
        @expected:
            (1) Current credit card information should not be present.
        """
        try:
            # steps
            admin_org_setting_page = LoginPage(self._driver).open()\
                .login(Constant.AdvanceOrgAdminEmail, Constant.DefaultPassword)\
                .goto_org_setting_page()\
                .open_billing_tab()\
                .open_change_card_details_dialog()\
                .clear_all_update_credit_card_info()\
                .fill_credit_card_info(Constant.Discover['number'],\
                                       Constant.Discover['name'],\
                                       Constant.Discover['exp_month'],\
                                       Constant.Discover['exp_year'],\
                                       Constant.Discover['security_code'])\
                .update_credit_card()
            # TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2472"
            self.assertTrue(False,"500 Error When saving credit card")
            self.assertTrue(admin_org_setting_page.is_new_credit_card_details_shown_up(\
                                       Constant.Discover['number'],\
                                       Constant.Discover['name'],\
                                       Constant.Discover['exp_month'],\
                                       Constant.Discover['exp_year']),\
                                       "The new credit card details doesn't show up on the main page or the card type icon hasn't changed")

            admin_org_setting_page.open_change_card_details_dialog()\
                .clear_all_update_credit_card_info()\
                .fill_credit_card_info(Constant.AmericanExpress['number'],\
                                       Constant.AmericanExpress['name'],\
                                       Constant.AmericanExpress['exp_month'],\
                                       Constant.AmericanExpress['exp_year'],\
                                       Constant.AmericanExpress['security_code'])\
                .update_credit_card()
            # TODO: This test case failed due to bug "https://jira.suitabletech.com/browse/INFR-2472"
            self.assertTrue(False,"500 Error When saving credit card")
            self.assertTrue(admin_org_setting_page.is_new_credit_card_details_shown_up(\
                                       Constant.AmericanExpress['number'],\
                                       Constant.AmericanExpress['name'],\
                                       Constant.AmericanExpress['exp_month'],\
                                       Constant.AmericanExpress['exp_year']),\
                                       "The new credit card details doesn't show up on the main page or the card type icon hasn't changed")
        finally:
            pass
