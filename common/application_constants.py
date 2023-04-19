# -*- coding: utf-8 -*-

class ApplicationConst(object):
    
    LBL_MANAGE_YOUR_BEAMS = u"" #"Manage Your Beams"
    LBL_DOWNLOAD_INSTALLER = u"" #"Download Installer"
    LBL_DOCUMENTATION = u"" #"Documentation"
    LBL_BEAM_HELP = u"" #"Beam Help Center"
    
    #Dashboard
    LBL_DASHBOARD_TEXT = u""#"Dashboard"
    SECT_WELCOME_TO_BEAM = u"" #"Welcome to Beam! You have successfully created your Beam account. Now take a look at the shortcuts to the right to begin your experience!"
    SECT_DOWNLOAD_AND_INSTALL = u"" #"Download and Install the Beam App This is required to use any Beam device. Once you've installed and opened this application you will see a list of any Beam devices you have been invited to use."
    SECT_LINK_A_NEW_BEAM = u"" #"Link a new Beam (that you own) to our network Or you can always use the 'Add new Beam' link below."
    
    #Beams Page
    LBL_BEAM_OFFLINE_STATUS = u""#"Offline"
    LBL_BEAM_AVAILABLE_STATUS = u""#"Available"
    LBL_LAST_USED = u""#"Last Used"
    LBL_STATUS = u""#"Status"
    #Application strings on Beams Settings page
    CHK_NOTIFY_REQUEST_ACCESS = u"" #"Notify administrators when someone requests access to this group"
    CHK_NOTIFY_ADMIN_IF_BEAM_LEFT_OFF_CHARGER = u"" #"Notify administrators if a Beam is left off the charger"
    CHK_NOTIFY_PILOT_IF_BEAM_LEFT_OFF_CHARGER = u"" #"Notify the last pilot if a Beam is left off the charger"
    LBL_SUCCESS_MESSAGE = u""#"Contextual Help Messages Reset"
    LBL_DISPLAY_URL_REQUEST = u""#"Display a URL Connection Invitation"

    #Application string on Org Billing page
    LBL_NAME_ON_CARD = u"" #"Name on Card"

    #Application string on Beams Access Times page
    LBL_ALL_MEMBERS = u"" #"All Members"

    #Application strings on Your Account -> Notifications page
    CHK_NOTIFY_BECOME_AN_ADMIN = u"" #"I become an administrator"
    CHK_NOTIFY_ADDED_OR_REMOVED_FROM_DEVICE_GROUP = u"" #"I am added to or removed from a device group"
    CHK_NOTIFY_DEVICE_MEMBERS_GROUP_ARE_ADDED_REMOVED = u"" # "Device group members are added or removed"
    CHK_NOTIFY_DEVICE_GROUPS_ARE_ADDED_REMOVED = u""
    CHK_NOTIFY_DEVICE_GROUPS_SETTINGS_ARE_CHANGED = u"" #Device group settings are changed
    CHK_NOTIFY_I_CAN_CHANGE_DEVICE_SETTINGS_OR_ANSWER_CALLS =u"" #I can change device settings or answer calls
    CHK_NOTIFY_I_RESERVE_BEAMS = u"" #I reserve Beams
    
    #Application string on User Group Detail page
    LBL_DEVICE_GROUPS_PROPERTY = u"" #"Device Groups"
    LBL_LOCATION_NAME = u"" #"Name"
    LBL_LOCATION_PROPERTY = u"" #"Location"
    LBL_LABEL_PROPERTY = u"" #"Labels"
    LBL_GROUP_PROPERTY = u"" #"Group"
    LBL_TIMEZONE_PROPERTY = u"" #"Time Zone"
    LBL_NONE_PROPERTY =u"" #"None"
    
    #Page Header labels
    LBL_ADMIN_USERS_SECTION_USERS = u"" #"Users"
    LBL_ACCOUNT_SETTINGS_PAGE_HEADER = u"" #"Account Settings"
    LBL_ACCOUNT_NOTIFICATIONS_PAGE_HEADER = u"" #"Notifications"
    LBL_ORG_SETTINGS_PAGE_HEADER = u"" #"Organization Settings"
    LBL_APPROVED_REQUEST_ACCESS_BEAM_HEADER = u"" #Approved
    LBL_REJECTED_REQUEST_ACCESS_BEAM_HEADER = u"" #Rejected
    LBL_ERROR_REQUEST_ACCESS_BEAM_HEADER = u""
    LBL_BEAMS_ACCESS_TIMES_TEMPORARY_USERS = u"" #"Temporary Users"
    LBL_BEAMS_DEVICES_PAGE_HEADER = u"" #"Devices in"
    LBL_BEAMS_MEMBERS_USERS = u"" #"Users"
    LBL_BEAMS_MEMBERS_USER_GROUPS = u"" #"User Groups"
    LBL_BEAMS_MEMBERS_REMOVE_USER = u"" #"Remove"
    LBL_PLAY_VIDEO_CONTINUE = u"" #"Continue"
    LBL_CONFIRM_NEW_AUTH_METHOD = u"" #"Confirm New Authentication Method"
    LBL_DISCONNECT_SUCCESSFUL = u"" #"Disconnect Successful"
    LBL_YES = u"" #"Yes"
    LBL_NO = u"" #"No"
    LBL_DELETE = u"" #"Delete"
    
    #Application strings on dialogs
    WARN_MSG_CHANGE_DEVICE_GROUP_NAME = u"" #"Warning! If you move this device to a different group, members of this group will no longer be able to access it."
    WARN_MSG_REMOVE_USER_GROUP = u"" # "Are you sure you want to remove this user group from the '{}' device group?"
    WARN_MSG_REMOVE_DEVICES_GROUP = u"" #Are you sure you want to delete this content? It is used in 1 places.
    WARN_MSG_USER_DOES_NOT_HAVE_ACCESS_DEVICE = u"" #This user does not have access to the requested device. An admin will need to add the user to the device group or a user group with access before this reservation will be accessible.
    
    #Application strings on warning message
    INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL = u"" #"The device group was successfully created."
    INFO_MSG_SAVE_DEVICE_GROUP_SETTING_SUCCESSFUL = u"" #"Device group settings were saved successfully."
    INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL = u"" #"The device was saved successfully."
    INFO_MSG_DELETE_USER_GROUP_SUCCESSFUL = u"" #"The group was successfully deleted."
    INFO_MSG_CREATE_USER_GROUP_SUCCESSFUL = u"" #"User group created successfully."
    INFO_MSG_INVITE_USER_TO_SIMPL_BEAM_SUCCESSFUL = u"" #"{} was added to {}."
    INFO_INVITATION_MAIL_SENT_SUCCESSFUL = "" #"The invitation to {} was successfully sent."
    INFO_MSG_NEW_API_NOTICE = u"" # Your new API Key is: (.*). Please copy this key \(without surrounding quotes\) and store it somewhere safe. Once you leave this page, you will no longer have access to the secret portion of this key. For more information on how to use API keys, please check out the Web API Documentation Page
    INFO_MSG_EDIT_USER_SUCCESS = u"" #The user was successfully saved.
    INFO_MSG_DEVICE_GROUP_EXISTED = u"" #A device group with that name already exists.
    INFO_MSG_USER_GROUP_EXISTED = u"" #A user group with that name already exists.
    INFO_MSG_INVITE_INVALID_EMAIL = u"" #Enter a valid email address.
    INFO_MOBILE_MSG_CREATE_API = u"" #API key generation not available on mobile site.
    
    #Device group
    DELETE_USER_FROM_DEVICE_GROUP = u"" #"Are you sure you want to remove this member from the '{}' device group?"
    LBL_DEVICE_GROUPS = u"" #"Device Groups"
    LBL_USER_GROUPS = u"" #"User Groups"
    LBL_ACCESS_REQUESTS = u"" #'Access Requests'
    #User group
    LBL_ALL_USERS_GROUP = u"" #"All Users"
    LBL_SAML_USERS_GROUP = u"" #"SAML Users"
    
    #User Detail Page
    LBL_ADMINISTERS_GROUPS = u"" #"Administers Groups"
    LBL_ADMINISTRATOR = u"" #"Administrator"
    LBL_MENU_ADMINISTRATOR_ONLY = u"" #"Administrators Only"
    LBL_MENU_GUEST_ONLY = u"" #"Guests Only"
    LBL_MENU_USER_GROUPS = u"" #"User Groups"
    LBL_MENU_TEMPORARY_USERS = u"" #"Temporary Users"
    LBL_100_ITEMS = u"" #"100 Items"
    LBL_10_ITEMS = u"" #"10 Items"
    LBL_MENU_ADD_ADD_ORGANIZATION_USERS = u"" #"Add All Organization Users"
    LBL_MENU_REMOVE_ALL_USERS = u"" #"Remove All Users"
    LST_MILESTONES = u"" #"Invited,Logged In,Agreement,Connected,Called"
    INFO_MSG_REMOVE_USER_FROM_ORG_SUCCESSFUL = u"" #"The user was successfully deleted."
    
    TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE = u"" #"WARNING: Only one authentication method is allowed per account. Your account is currently authenticated with a Suitable Technologies username and password. Continuing will cause your account to be authenticated via Google.\nOnce you change your authentication method to Google, you will no longer be able to login to the website or Beam client using your Suitable Technologies username and password. You will need to click \"Sign in with Google\" from now on. You must also have an up-to-date version of the client.\nDo you really want to change your authentication method to Google?\nYes No"

    #Others
    LBL_IMAGE_CROP_TRACKER = u"" #"Select the area you would like to use"
    LBL_ACCESS_REQUEST_RECORD_MESSAGE = u"" #requests to be added to group
    LBL_APPROVED_NOTIFICATION_MESSAGE = u"The access request has been approved."
    LBL_REJECTED_NOTIFICATION_MESSAGE = u"The access request has been rejected."
    LBL_IMPORT_CONTACT_ERROR_MESSAGE = u"There was an error importing your contacts."
    LBL_DELETE_ERROR_MESSAGE = u"There was an error with your request. Please try again later."
    CHK_ALL_AUTHENTICATION_METHODS = u"" # All authentication methods
    LBL_WELCOME_TO_BEAM_EMAIL_TITLE = u""
    LBL_BEAM_ALL_AUTHENTICATION_METHODS = u""
    LBL_WELCOME_TEMPORARY_USER_EMAIL_TITLE = u""
    
    #Date-time
    LBL_DATETIME_MERIDIAN_AM = u"" #"AM"
    LBL_DATETIME_MERIDIAN_PM = u"" #"PM"
    
    #Reservation
    LBL_RESERVATION_SERVER_ADDRESS = u""
    LBL_RESERVATION_PASSWORD = u""
    LBL_RESERVATION_USER_NAME = u""
    LBL_RESERVATION_TAB = u"" #"Reservations"
    LBL_RESERVATION_REJECTED_STATUS = u"Rejected"
    LBL_RESERVATION_CONFIRMED_STATUS = u"Confirmed"
    LBL_RESERVATION_REQUESTED_STATUS = u"Requested"
    INFO_MSG_CREATE_RESERVATION_SUCCESSFUL = u"The reservation was created."
    INFO_MSG_DELETE_RESERVATION_SUCCESSFUL = u"The reservation was deleted."
    INFO_MSG_EDIT_RESERVATION_SUCCESSFUL = u"The reservation was changed."
    INFO_MSG_REJECT_RESERVATION_SUCCESSFUL = u"The reservation was rejected."
    INFO_MOBILE_MSG_REJECT_RESERVATION_SUCCESSFUL = u"The reservation was rejected."
    INFO_MSG_REQUEST_RESERVATION_SUCCESSFUL = u"Your request was sent."
    
    LBL_LINKING_CODE_ERROR = u"" #"The code you entered was not valid. Please enter the 6-digit code shown on your device's screen."
    LBL_ALLOWED = u""
    LBL_NOT_ALLOWED = u""
    LBL_BY_REQUEST = u""
    LBL_BY_ADMINISTRATORS_ONLY = u""
    STATE_IN_A_CALL = u""
    STATE_MISSED_CALLS = u""
    STATE_OFFLINE = u""
    STATE_CONFIGURING = u""
    STATE_UPGRADING = u""
    
    #Device Settings Advance Dialog
    LBL_SYSTEM = u"" #System
    LBL_SERIAL_NUMBER = u"" #Serial Number
    LBL_UID = u"" #UID
    LBL_SOFTWARE_VERSION = u"" #Software Version
    LBL_LINKED_BY = u"" #Linked By
    LBL_LINKED_ON = u"" #Linked On
    
    LBL_NETWORK = u"" #Network
    LBL_FREQUENCY = u"" #Frequency
    LBL_TYPE = u"" #Type
    LBL_IP_ADDRESS = u"" #IP Address

    #Tooltip
    CONTENT_OF_TOOLTIP = u""
    
    _date_time_localized_values = {}
    
    @staticmethod
    def initialize():
        ApplicationConst.LBL_DASHBOARD_TEXT = _("LBL_DASHBOARD_TEXT")
        ApplicationConst.SECT_WELCOME_TO_BEAM = _("SECT_WELCOME_TO_BEAM")
        ApplicationConst.SECT_DOWNLOAD_AND_INSTALL = _("SECT_DOWNLOAD_AND_INSTALL")
        ApplicationConst.SECT_LINK_A_NEW_BEAM = _("SECT_LINK_A_NEW_BEAM")
        ApplicationConst.LBL_BEAM_OFFLINE_STATUS = _("LBL_BEAM_OFFLINE_STATUS")
        ApplicationConst.LBL_BEAM_AVAILABLE_STATUS = _("LBL_BEAM_AVAILABLE_STATUS")
        ApplicationConst.LBL_MANAGE_YOUR_BEAMS = _("LBL_MANAGE_YOUR_BEAMS")
        ApplicationConst.LBL_ACCOUNT_SETTINGS = _("LBL_ACCOUNT_SETTINGS")
        ApplicationConst.LBL_DOWNLOAD_INSTALLER = _("LBL_DOWNLOAD_INSTALLER")
        ApplicationConst.LBL_DOCUMENTATION = _("LBL_DOCUMENTATION")
        ApplicationConst.LBL_BEAM_HELP = _("LBL_BEAM_HELP")
        ApplicationConst.LBL_DEVICES = _("LBL_DEVICES")
        ApplicationConst.LBL_STATUS = _("LBL_STATUS")
        ApplicationConst.LBL_LAST_USED = _("LBL_LAST_USED")

        ApplicationConst.CHK_NOTIFY_REQUEST_ACCESS = _("CHK_NOTIFY_REQUEST_ACCESS")
        ApplicationConst.CHK_NOTIFY_ADMIN_IF_BEAM_LEFT_OFF_CHARGER = _("CHK_NOTIFY_ADMIN_IF_BEAM_LEFT_OFF_CHARGER")
        ApplicationConst.CHK_NOTIFY_PILOT_IF_BEAM_LEFT_OFF_CHARGER = _("CHK_NOTIFY_PILOT_IF_BEAM_LEFT_OFF_CHARGER")
        ApplicationConst.LBL_SUCCESS_MESSAGE = _("LBL_SUCCESS_MESSAGE")
        ApplicationConst.LBL_DISPLAY_URL_REQUEST = _("LBL_DISPLAY_URL_REQUEST")
        ApplicationConst.LBL_NAME_ON_CARD = _("LBL_NAME_ON_CARD")
        ApplicationConst.LBL_ALL_MEMBERS = _("LBL_ALL_MEMBERS")
        ApplicationConst.CHK_NOTIFY_BECOME_AN_ADMIN = _("CHK_NOTIFY_BECOME_AN_ADMIN")
        ApplicationConst.CHK_NOTIFY_ADDED_OR_REMOVED_FROM_DEVICE_GROUP = _("CHK_NOTIFY_ADDED_OR_REMOVED_FROM_DEVICE_GROUP")
        ApplicationConst.CHK_NOTIFY_DEVICE_MEMBERS_GROUP_ARE_ADDED_REMOVED = _("CHK_NOTIFY_DEVICE_MEMBERS_GROUP_ARE_ADDED_REMOVED")
        ApplicationConst.CHK_NOTIFY_DEVICE_GROUPS_ARE_ADDED_REMOVED = _("CHK_NOTIFY_DEVICE_GROUPS_ARE_ADDED_REMOVED")
        ApplicationConst.CHK_NOTIFY_DEVICE_GROUPS_SETTINGS_ARE_CHANGED = _("CHK_NOTIFY_DEVICE_GROUPS_SETTINGS_ARE_CHANGED")
        ApplicationConst.CHK_NOTIFY_I_CAN_CHANGE_DEVICE_SETTINGS_OR_ANSWER_CALLS = _("CHK_NOTIFY_I_CAN_CHANGE_DEVICE_SETTINGS_OR_ANSWER_CALLS")
        ApplicationConst.CHK_NOTIFY_I_RESERVE_BEAMS = _("CHK_NOTIFY_I_RESERVE_BEAMS")
       
        ApplicationConst.LBL_DEVICE_GROUPS_PROPERTY = _("LBL_DEVICE_GROUPS_PROPERTY")
        ApplicationConst.LBL_LOCATION_NAME = _("LBL_LOCATION_NAME")
        ApplicationConst.LBL_LOCATION_PROPERTY = _("LBL_LOCATION_PROPERTY")
        ApplicationConst.LBL_LABEL_PROPERTY = _("LBL_LABEL_PROPERTY")
        ApplicationConst.LBL_GROUP_PROPERTY = _("LBL_GROUP_PROPERTY")
        ApplicationConst.LBL_TIMEZONE_PROPERTY = _("LBL_TIMEZONE_PROPERTY")
        ApplicationConst.LBL_NONE_PROPERTY =_("LBL_NONE_PROPERTY")
        ApplicationConst.LBL_ADMIN_USERS_SECTION_USERS = _("LBL_ADMIN_USERS_SECTION_USERS")
        ApplicationConst.LBL_ACCOUNT_SETTINGS_PAGE_HEADER = _("LBL_ACCOUNT_SETTINGS_PAGE_HEADER")
        ApplicationConst.LBL_ACCOUNT_NOTIFICATIONS_PAGE_HEADER = _("LBL_ACCOUNT_NOTIFICATIONS_PAGE_HEADER")
        ApplicationConst.LBL_ORG_SETTINGS_PAGE_HEADER = _("LBL_ORG_SETTINGS_PAGE_HEADER")
        ApplicationConst.LBL_APPROVED_REQUEST_ACCESS_BEAM_HEADER = _("LBL_APPROVED_REQUEST_ACCESS_BEAM_HEADER")
        ApplicationConst.LBL_REJECTED_REQUEST_ACCESS_BEAM_HEADER = _("LBL_REJECTED_REQUEST_ACCESS_BEAM_HEADER")
        ApplicationConst.LBL_ERROR_REQUEST_ACCESS_BEAM_HEADER = _("LBL_ERROR_REQUEST_ACCESS_BEAM_HEADER")
        ApplicationConst.LBL_BEAMS_ACCESS_TIMES_TEMPORARY_USERS = _("LBL_BEAMS_ACCESS_TIMES_TEMPORARY_USERS")
        ApplicationConst.LBL_BEAMS_DEVICES_PAGE_HEADER = _("LBL_BEAMS_DEVICES_PAGE_HEADER")
        ApplicationConst.LBL_BEAMS_MEMBERS_USERS = _("LBL_BEAMS_MEMBERS_USERS")
        ApplicationConst.LBL_BEAMS_MEMBERS_USER_GROUPS = _("LBL_BEAMS_MEMBERS_USER_GROUPS")
        ApplicationConst.LBL_BEAMS_MEMBERS_REMOVE_USER = _("LBL_BEAMS_MEMBERS_REMOVE_USER")
        
        # MISC LABELS
        ApplicationConst.LBL_PLAY_VIDEO_CONTINUE = _("LBL_PLAY_VIDEO_CONTINUE")
        ApplicationConst.LBL_CONFIRM_NEW_AUTH_METHOD = _("LBL_CONFIRM_NEW_AUTH_METHOD")
        ApplicationConst.LBL_DISCONNECT_SUCCESSFUL = _("LBL_DISCONNECT_SUCCESSFUL")
        ApplicationConst.LBL_YES = _("LBL_YES")
        ApplicationConst.LBL_NO = _("LBL_NO")
        ApplicationConst.LBL_DELETE_ERROR_MESSAGE = _("LBL_DELETE_ERROR_MESSAGE")
        
        #Application strings on dialogs/toast messages
        ApplicationConst.INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL = _("INFO_MSG_CREATE_DEVICE_GROUP_SUCCESSFUL")
        ApplicationConst.INFO_MSG_SAVE_DEVICE_GROUP_SETTING_SUCCESSFUL = _("INFO_MSG_SAVE_DEVICE_GROUP_SETTING_SUCCESSFUL")
        ApplicationConst.INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL = _("INFO_MSG_SET_DEVICE_GROUP_SUCCESSFUL")
        ApplicationConst.WARN_MSG_CHANGE_DEVICE_GROUP_NAME = _("WARN_MSG_CHANGE_DEVICE_GROUP_NAME")
        ApplicationConst.WARN_MSG_REMOVE_USER_GROUP = _("WARN_MSG_REMOVE_USER_GROUP")
        ApplicationConst.WARN_MSG_REMOVE_DEVICES_GROUP = _("WARN_MSG_REMOVE_DEVICES_GROUP")
        ApplicationConst.WARN_MSG_USER_DOES_NOT_HAVE_ACCESS_DEVICE = _("WARN_MSG_USER_DOES_NOT_HAVE_ACCESS_DEVICE")
        ApplicationConst.INFO_MSG_DELETE_USER_GROUP_SUCCESSFUL = _("INFO_MSG_DELETE_USER_GROUP_SUCCESSFUL")
        ApplicationConst.INFO_MSG_CREATE_USER_GROUP_SUCCESSFUL = _("INFO_MSG_CREATE_USER_GROUP_SUCCESSFUL")
        ApplicationConst.INFO_MSG_INVITE_USER_TO_SIMPL_BEAM_SUCCESSFUL = _("INFO_MSG_INVITE_USER_TO_SIMPL_BEAM_SUCCESSFUL")
        ApplicationConst.INFO_INVITATION_MAIL_SENT_SUCCESSFUL = _("INFO_INVITATION_MAIL_SENT_SUCCESSFUL")
        ApplicationConst.INFO_MSG_NEW_API_NOTICE = _("INFO_MSG_NEW_API_NOTICE")
        ApplicationConst.INFO_MSG_NEW_API_NOTICE_2 = _("INFO_MSG_NEW_API_NOTICE_2")
        ApplicationConst.INFO_MSG_EDIT_USER_SUCCESS = _("INFO_MSG_EDIT_USER_SUCCESS")
        ApplicationConst.INFO_MSG_DEVICE_GROUP_EXISTED = _("INFO_MSG_DEVICE_GROUP_EXISTED")
        ApplicationConst.INFO_MSG_USER_GROUP_EXISTED = _("INFO_MSG_USER_GROUP_EXISTED")
        ApplicationConst.INFO_MSG_INVITE_INVALID_EMAIL = _("INFO_MSG_INVITE_INVALID_EMAIL")
        ApplicationConst.INFO_MOBILE_MSG_CREATE_API = _("INFO_MOBILE_MSG_CREATE_API")
        
        #Device group
        ApplicationConst.DELETE_USER_FROM_DEVICE_GROUP = _("DELETE_USER_FROM_DEVICE_GROUP")
        ApplicationConst.LBL_DEVICE_GROUPS = _("LBL_DEVICE_GROUPS")
        ApplicationConst.LBL_USER_GROUPS = _("LBL_USER_GROUPS")
        ApplicationConst.LBL_ACCESS_REQUESTS = _("LBL_ACCESS_REQUESTS")
        
        #User Group
        ApplicationConst.LBL_ALL_USERS_GROUP = _("LBL_ALL_USERS_GROUP")
        ApplicationConst.LBL_SAML_USERS_GROUP = _("LBL_SAML_USERS_GROUP")
        
        #User Detail Page
        ApplicationConst.LBL_ADMINISTERS_GROUPS = _("LBL_ADMINISTERS_GROUPS")
        ApplicationConst.LBL_ADMINISTRATOR = _("LBL_ADMINISTRATOR")
        ApplicationConst.LBL_MENU_ADMINISTRATOR_ONLY = _("LBL_MENU_ADMINISTRATOR_ONLY")
        ApplicationConst.LBL_MENU_GUEST_ONLY = _("LBL_MENU_GUEST_ONLY")
        ApplicationConst.LBL_MENU_USER_GROUPS = _("LBL_MENU_USER_GROUPS")
        ApplicationConst.LBL_MENU_TEMPORARY_USERS = _("LBL_MENU_TEMPORARY_USERS")
        ApplicationConst.LST_MILESTONES = _("LST_MILESTONES")
        ApplicationConst.INFO_MSG_REMOVE_USER_FROM_ORG_SUCCESSFUL = _("INFO_MSG_REMOVE_USER_FROM_ORG_SUCCESSFUL")
        ApplicationConst.TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE = _("TXTF_CONFIRM_ASSOCIATION_WARNING_MESSAGE")
        ApplicationConst.LBL_100_ITEMS = _("LBL_100_ITEMS")
        ApplicationConst.LBL_10_ITEMS = _("LBL_10_ITEMS")
        ApplicationConst.LBL_MENU_ADD_ADD_ORGANIZATION_USERS = _("LBL_MENU_ADD_ADD_ORGANIZATION_USERS")
        ApplicationConst.LBL_MENU_REMOVE_ALL_USERS = _("LBL_MENU_REMOVE_ALL_USERS")
        #Google Page
        ApplicationConst.LBL_ERROR_MESSAGE = _("LBL_ERROR_MESSAGE")
        
        #Others
        ApplicationConst.LBL_IMAGE_CROP_TRACKER = _("LBL_IMAGE_CROP_TRACKER")
        ApplicationConst.LBL_ACCESS_REQUEST_RECORD_MESSAGE = _("LBL_ACCESS_REQUEST_RECORD_MESSAGE")
        ApplicationConst.LBL_APPROVED_NOTIFICATION_MESSAGE = _("LBL_APPROVED_NOTIFICATION_MESSAGE")
        ApplicationConst.LBL_REJECTED_NOTIFICATION_MESSAGE = _("LBL_REJECTED_NOTIFICATION_MESSAGE")
        ApplicationConst.LBL_IMPORT_CONTACT_ERROR_MESSAGE = _("LBL_IMPORT_CONTACT_ERROR_MESSAGE")
        ApplicationConst.CHK_ALL_AUTHENTICATION_METHODS = _("CHK_ALL_AUTHENTICATION_METHODS")
        ApplicationConst.LBL_WELCOME_TO_BEAM_EMAIL_TITLE = _("LBL_WELCOME_TO_BEAM_EMAIL_TITLE")
        ApplicationConst.LBL_BEAM_ALL_AUTHENTICATION_METHODS = _("LBL_BEAM_ALL_AUTHENTICATION_METHODS")
        ApplicationConst.LBL_WELCOME_TEMPORARY_USER_EMAIL_TITLE = _("LBL_WELCOME_TEMPORARY_USER_EMAIL_TITLE")
        
        #Date-time
        ApplicationConst.LBL_DATETIME_MERIDIAN_AM = _("LBL_DATETIME_MERIDIAN_AM")
        ApplicationConst.LBL_DATETIME_MERIDIAN_PM = _("LBL_DATETIME_MERIDIAN_PM")
        ApplicationConst.LBL_RESERVATION_SERVER_ADDRESS = _("LBL_RESERVATION_SERVER_ADDRESS")
        
        #Reservation
        ApplicationConst.LBL_RESERVATION_PASSWORD = _("LBL_RESERVATION_PASSWORD")
        ApplicationConst.LBL_RESERVATION_USER_NAME = _("LBL_RESERVATION_USER_NAME")
        ApplicationConst.LBL_RESERVATION_TAB = _("LBL_RESERVATION_TAB")
        ApplicationConst.LBL_RESERVATION_REJECTED_STATUS = _("LBL_RESERVATION_REJECTED_STATUS")
        ApplicationConst.LBL_RESERVATION_CONFIRMED_STATUS  = _("LBL_RESERVATION_CONFIRMED_STATUS")
        ApplicationConst.LBL_RESERVATION_REQUESTED_STATUS  = _("LBL_RESERVATION_REQUESTED_STATUS")
        ApplicationConst.INFO_MSG_CREATE_RESERVATION_SUCCESSFUL = _("INFO_MSG_CREATE_RESERVATION_SUCCESSFUL")
        ApplicationConst.INFO_MSG_DELETE_RESERVATION_SUCCESSFUL = _("INFO_MSG_DELETE_RESERVATION_SUCCESSFUL")
        ApplicationConst.INFO_MSG_EDIT_RESERVATION_SUCCESSFUL = _("INFO_MSG_EDIT_RESERVATION_SUCCESSFUL")
        ApplicationConst.INFO_MSG_REJECT_RESERVATION_SUCCESSFUL = _("INFO_MSG_REJECT_RESERVATION_SUCCESSFUL")
        ApplicationConst.INFO_MOBILE_MSG_REJECT_RESERVATION_SUCCESSFUL = _("INFO_MOBILE_MSG_REJECT_RESERVATION_SUCCESSFUL")
        ApplicationConst.INFO_MSG_REQUEST_RESERVATION_SUCCESSFUL = _("INFO_MSG_REQUEST_RESERVATION_SUCCESSFUL")
        ApplicationConst.LBL_LINKING_CODE_ERROR = _("LBL_LINKING_CODE_ERROR")
        ApplicationConst.LBL_DELETE = _("LBL_DELETE")
        ApplicationConst.LBL_ALLOWED = _("LBL_ALLOWED")
        ApplicationConst.LBL_NOT_ALLOWED = _("LBL_NOT_ALLOWED")
        ApplicationConst.LBL_BY_REQUEST = _("LBL_BY_REQUEST")
        ApplicationConst.LBL_BY_ADMINISTRATORS_ONLY = _("LBL_BY_ADMINISTRATORS_ONLY")
        ApplicationConst.STATE_IN_A_CALL = _("STATE_IN_A_CALL")
        ApplicationConst.STATE_MISSED_CALLS = _("STATE_MISSED_CALLS")
        ApplicationConst.STATE_OFFLINE = _("STATE_OFFLINE")
        ApplicationConst.STATE_CONFIGURING = _("STATE_CONFIGURING")
        ApplicationConst.STATE_UPGRADING = _("STATE_UPGRADING")

        #Device Settings Advance Dialog
        ApplicationConst.LBL_SYSTEM = _("LBL_SYSTEM")
        ApplicationConst.LBL_SERIAL_NUMBER = _("LBL_SERIAL_NUMBER")
        ApplicationConst.LBL_UID = _("LBL_UID")
        ApplicationConst.LBL_SOFTWARE_VERSION = _("LBL_SOFTWARE_VERSION")
        ApplicationConst.LBL_LINKED_BY = _("LBL_LINKED_BY")
        ApplicationConst.LBL_LINKED_ON = _("LBL_LINKED_ON")
        ApplicationConst.LBL_NETWORK = _("LBL_NETWORK")
        ApplicationConst.LBL_FREQUENCY = _("LBL_FREQUENCY")
        ApplicationConst.LBL_TYPE = _("LBL_TYPE")
        ApplicationConst.LBL_IP_ADDRESS = _("LBL_IP_ADDRESS")

        #Tooltip
        ApplicationConst.CONTENT_OF_TOOLTIP = _("CONTENT_OF_TOOLTIP")
        
    @staticmethod
    def initialize_date_time_localization():
        ApplicationConst._date_time_localized_values["MON01"] = _("MON01")
        ApplicationConst._date_time_localized_values["MON02"] = _("MON02")
        ApplicationConst._date_time_localized_values["MON03"] = _("MON03")
        ApplicationConst._date_time_localized_values["MON04"] = _("MON04")
        ApplicationConst._date_time_localized_values["MON05"] = _("MON05")
        ApplicationConst._date_time_localized_values["MON06"] = _("MON06")
        ApplicationConst._date_time_localized_values["MON07"] = _("MON07")
        ApplicationConst._date_time_localized_values["MON08"] = _("MON08")
        ApplicationConst._date_time_localized_values["MON09"] = _("MON09")
        ApplicationConst._date_time_localized_values["MON10"] = _("MON10")
        ApplicationConst._date_time_localized_values["MON11"] = _("MON11")
        ApplicationConst._date_time_localized_values["MON12"] = _("MON12")
        
        ApplicationConst._date_time_localized_values["Jan"] = _("Jan")
        ApplicationConst._date_time_localized_values["Feb"] = _("Feb")
        ApplicationConst._date_time_localized_values["Mar"] = _("Mar")
        ApplicationConst._date_time_localized_values["Apr"] = _("Apr")
        ApplicationConst._date_time_localized_values["May"] = _("May")
        ApplicationConst._date_time_localized_values["Jun"] = _("Jun")
        ApplicationConst._date_time_localized_values["Jul"] = _("Jul")
        ApplicationConst._date_time_localized_values["Aug"] = _("Aug")
        ApplicationConst._date_time_localized_values["Sep"] = _("Sep")
        ApplicationConst._date_time_localized_values["Sept"] = _("Sept")
        ApplicationConst._date_time_localized_values["Oct"] = _("Oct")
        ApplicationConst._date_time_localized_values["Nov"] = _("Nov")
        ApplicationConst._date_time_localized_values["Dec"] = _("Dec")
        
        ApplicationConst._date_time_localized_values["Mon"] = _("Mon")
        ApplicationConst._date_time_localized_values["Tue"] = _("Tue")
        ApplicationConst._date_time_localized_values["Wed"] = _("Wed")
        ApplicationConst._date_time_localized_values["Thu"] = _("Thu")
        ApplicationConst._date_time_localized_values["Fri"] = _("Fri")
        ApplicationConst._date_time_localized_values["Sat"] = _("Sat")
        ApplicationConst._date_time_localized_values["Sun"] = _("Sun")
        ApplicationConst._date_time_localized_values["AM"] = _("AM")
        ApplicationConst._date_time_localized_values["PM"] = _("PM")
        ApplicationConst._date_time_localized_values["All day"] = _("All day")
        ApplicationConst._date_time_localized_values["every day"] = _("every day")
        ApplicationConst._date_time_localized_values["a day"] = _("a day")
        ApplicationConst._date_time_localized_values["days"] = _("days")
        ApplicationConst._date_time_localized_values["an hour"] = _("an hour")
        ApplicationConst._date_time_localized_values["hour"] = _("hours")
        ApplicationConst._date_time_localized_values["a minute"] = _("a minute")
        ApplicationConst._date_time_localized_values["minutes"] = _("minutes")
        ApplicationConst._date_time_localized_values["a few seconds"] = _("a few seconds")
       
    @staticmethod
    def get_date_time_label(english_text):
        return ApplicationConst._date_time_localized_values[english_text]
    