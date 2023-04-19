'''
Created on Aug 27, 2016

@author: ngocquang.tran
'''
class EmailDetailConstants(object):
    WelcomeEmailTitle = u"Welcome to Beam at {}"  # requires Organization Name
    WelcomeEmailContent = "\r\n{},\r\n\r\n{} invited you to Beam into {}.\n\n\nTo get started, visit this link to activate your account and set a password.\r\n\r\n{}/accounts/reset/(.*)/?new=1\r\n\r\nThis link expires in 7 days.\r\n\r\nYour username is your email address: {}\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\nThanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r"
    DownloadInstallSoftwareLink = u"If you haven't installed the Beam software on your computer yet, visit the following link to get started:https://stg1.suitabletech.com/installers"
    WelcomeSimplifiedEmailContent = r"\r\n\r\n{},\r\n\r\n{} invited you to Beam into {}.\r\n\r\nHello\r\n\r\n\r\nYou can log in with the following temporary password:Email address: {}Temporary password: (.*)This temporary password expires in 7 days.Thanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n"
    ResentWelcomeSimplifiedEmailContent = r"\r\n\r\n{},\r\n\r\n{} invited you to Beam into {}.\r\n\r\nHello\r\n\r\n\r\nYou can use your existing account with the username: {}You can find your temporary password in our earlier email.Thanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n"
    WelcomeExistingEmailContent = u"\r\n\r\n{},\r\n\r\n{} invited you to Beam into {}.\r\n\r\n\r\n\r\n\r\nYou can use your existing account with the username: {}\r\n\r\n\r\n\r\n\r\nYou can see which devices are available to use by signing in to the Beam software on your computer or mobile device.\r\n\r\n\r\n\r\n\r\nThanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n"
    
    WelcomeTemporaryUserEmailTitle = u"You've been invited to Beam into {}"  # requires Organization Name
    WelcomeTemporaryUserEmailContent = r"^\n\n{},\n\n{} invited you to Beam into {}.\n\nHello\n\n\nTo get started, visit this link to activate your account and set a password.\n\n{}/accounts/reset/(.*)/?new=1\n\nThis link expires in 7 days.\n\n\n\nYour username is your email address: {}\n\nIf you haven't installed the Beam software on your computer yet, visit the following link to get started:\nhttps://stg1.suitabletech.com/installers\n\n{}\n\n{}\n\nYou can Beam in during the following time period:\nBeginning: {}\nEnding: {}\nThese times are in the time zone of the device to which you're connecting.\n\n\n\nThanks,\n{}\n\nSuitable Technologies, Inc.\n921 E Charleston Rd\nPalo Alto, CA 94303\n1-855-200-2326\n$"
    # "\r\n\r\n{},\r\n\r\n{} invited you to Beam into {}.\r\n\r\nHello\r\n\r\n\r\nTo get started, visit this link to activate your account and set a password.\r\n\r\n{}/accounts/reset/(.*)/\?new=1\r\n\r\nThis link expires in 7 days.\r\n\r\n\r\n\r\nYour username is your email address: {}\r\n\r\n\r\n\r\n{}:\r\n\r\n{}\r\n\r\n\r\n\r\nYou can Beam in during the following time period:\r\nBeginning: {}\r\nEnding: {}\r\nThese times are in the time zone of the device to which you're connecting.\r\n\r\n\r\n\r\nThanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n$"
    # requires User Full Name, Admin Full Name, Organization Name, ST URL, User email address, Beam number, Beams list with "(America/Los_Angeles)", start time, end time, Admin Full Name
    
    WelcomeAdminCopyEmailTitle = u"Welcome to Beam at {} (copy)"  # requires Organization Name
    WelcomeAdminCopyEmailContent = u"\r\n\r\n----------\r\nThe following is your requested copy of the email sent to {}.\r\n----------\r\n\r\n{},\r\n\r\n{} invited you to Beam into {}.\r\n\r\nHello\r\n\r\n\r\nTo get started, visit this link to activate your account and set a password.\r\n\r\n[Link Removed]\r\n\r\nThis link expires in 7 days.\r\n\r\n\r\n\r\nYour username is your email address: {}\r\n\r\n\r\n\r\n\r\n\r\n\r\nThanks,\r\n{}\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n"
    # requires User email address, User Displayed name, Admin Full Name, Org name, User email address, Admin Full Name
    
    BeamRequestAccessEmailTitle = u"[Beam] Someone is requesting access to your Beams"
    BeamRequestAccessEmailContent = r"^\r\nSomeone is requesting access to your Beams\r\n\r\n\r\n\r\n{} has requested access to {}.\r\n\r\n\r\n\r\n\r\n\r\n{}\r\nTo approve this request, click on the link below:\r\n{}/r/(.*)/a/\r\n\r\nOtherwise, reject this request by clicking the link below:\r\n{}/r/(.*)/r/\r\n\r\n\r\nHave questions\? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires user full name (if user having) and User email address, Device group name, request message (Message:\r\nHello\r\n\r\n), ST URL, ST URL, ST URL
    
    AddedToDeviceGroupEmailTitle = u"[Beam] You have been added to {}"  # requires Devices Group Name
    AddedToDeviceGroupEmailContent = u"\r\nYou have been added to {}\r\n\r\n\r\n{} added you to {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device group name, Admin Full Name, Device group name, ST URL
    
    NotificationAddedToDeviceGroupEmailTitle = u"[Beam] A user was added to {}"  # requires Devices Group Name
    NotificationAddedToDeviceGroupEmailContent = u"\nA user was added to {}\n\n\n{} added {} to {}.\n\n\n\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\n\nYou can change your email notification settings here: {}/manage/#/account/notifications/\n\n\n\nThanks,\nSuitable Technologies\n\nSuitable Technologies, Inc.\n921 E Charleston Rd\nPalo Alto, CA 94303\n1-855-200-2326"
    # requires Device group name, Admin Full Name, User Full Name, Device group name, ST URL
    
    RemovedFromDeviceGroupEmailTitle = u"[Beam] You have been removed from {}"  # requires Devices Group Name
    RemovedFromDeviceGroupEmailContent = u"\r\nYou have been removed from {}\r\n\r\n\r\n{} removed you from {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device group name, Admin Full Name, Device group name, ST URL
    
    ManageDeviceGroupEmailTitle = u"[Beam] You can now manage {}"  # requires Devices Group Name
    ManageDeviceGroupEmailContent = u"\r\nYou can now manage {}\r\n\r\n\r\n{} added you to the list of users who can manage {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device group name, Admin Full Name, Device group name, ST URL
    
    RemovedFromOrgAdminEmailTitle = u"[Beam] You are no longer an administrator for {}"  # requires Organization Name
    RemovedFromOrgAdminEmailContent = u"\r\nYou are no longer an administrator for {}\r\n\r\n\r\n{} removed you from the list of {} administrators.\r\n\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Organization Name, Admin Full Name, Organization Name, ST URL
    
    AddedToOrgAdminEmailTitle = u"[Beam] You are now an administrator of {}"  # requires Organization Name
    AddedToOrgAdminEmailContent = u"\r\nYou are now an administrator of {}\r\n\r\n\r\n{} made you an administrator of {}.\r\n\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Organization Name, Admin Full Name, Organization Name, ST URL
    
    TemporaryAccessTimeHasChangedTitle = u"[Beam] Your temporary access time for {} has changed"  # requires Device Group Name
    TemporaryAccessTimeHasChangedContent = u"\r\nYour temporary access time for {} has changed\r\n\r\n\r\n{} changed your access time(s) for {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device Group Name, Admin Full name, Device Group Name, ST URL
    
    BeamRemovedFromDeviceGroupTitle = u"[Beam] A Beam was removed from {}"  # requires Device Group Name
    BeamRemovedFromDeviceGroupContent = u"\r\nA Beam was removed from {}\r\n\r\n\r\n{} removed {} from {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device Group Name, Admin Full name (who added new device group), Beam name, Device Group Name, ST URL
    
    AddToUserGroupEmailTitle = u"[Beam] You have been added to the group {}"  # require User Group
    AddToUserGroupEmailContent = u"\r\nYou have been added to the group {}\r\n\r\n\r\n{} added you to the user group {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: https://staging.suitabletech.com/manage/#/account/notifications/\r\n\r\n\r\n\r\n\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires User Group  Name, Admin Full name (who added new user group)
    
    PasswordChangedEmailTitle = u"Your password has changed"
    PasswordChangedEmailContent = u"\r\nYour password for Beam and suitabletech.com has been changed.\r\nYour username:\r\n{}\r\n\r\nIf you believe this is in error, please contact support@suitabletech.com.\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\nThanks,\r\nSuitable Technologies Support\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n"
    # requires User email address, ST URL
    
    PasswordResetEmailTitle = u"Beam Password Reset"
    PasswordResetEmailContent = r"^\r\nYou're receiving this e-mail because you requested a password reset for your user account at Suitable Technologies.\r\n\r\nPlease go to the following page and choose a new password:\r\n\r\n{}/accounts/reset/(.*)/\r\n\r\nYour username, in case you've forgotten: {}\r\n\r\n\r\nThanks,\r\nSuitable Technologies Support\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326\r\n\r\n$"
    # requires ST URL, User email address,
    
    CanNowAcceptSessionsEmailTitle = u"[Beam] You can now accept sessions for {}" # requires Device Group Name
    CanNowAcceptSessionsEmailContent = u"\r\nYou can now accept sessions for {}\r\n\r\n\r\n{} added you to the list of users who can answer session requests for {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device Group Name, Admin Full name, Device Group Name, ST URL
    
    CanNoLongerAcceptSessionsEmailTitle = u"[Beam] You can no longer accept sessions for {}" # requires Device Group Name
    CanNoLongerAcceptSessionsEmailContent = u"\r\nYou can no longer accept sessions for {}\r\n\r\n\r\n{} removed you from the list of users who can answer session requests for {}.\r\n\r\n\r\n\r\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\r\n\r\nYou can change your email notification settings here: {}/manage/#/account/notifications/\r\n\r\n\r\n\r\nThanks,\r\nSuitable Technologies\r\n\r\nSuitable Technologies, Inc.\r\n921 E Charleston Rd\r\nPalo Alto, CA 94303\r\n1-855-200-2326"
    # requires Device Group Name, Admin Full name, Device Group Name, ST URL
    
    GoogleChangeAuthEmailTitle = u"Your authentication method has been changed"
    GoogleChangeAuthEmailContent = u"User account: {}\r\n\r\nThis email acknowledges that you have disconnected your Beam account from Google.\r\n\r\nIf you wish to sign in with a Suitable Technologies username and password, you must first reset your password: {}/accounts/password_reset/.\r\n\r\nIf you believe this is in error, please contact support@suitabletech.com.\r\n"
    # requires reciever email, ST URL    
    GoogleChangeAuthConnectEmailContent = u"User account: {}\r\n\r\nThis email acknowledges that your authentication method has been changed to Google. You must use Google to login to the website and Beam client from now on.\r\n\r\nIf you believe this is in error, please contact support@suitabletech.com.\r\n"
    # requires reciever email
    
    DeleteDeviceGroupEmailTitle = u"[Beam] A device group was removed from {}" # requires Organization Name
    DeleteDeviceGroupEmailContent = u"\nA device group was removed from {}\n\n\n{} removed the device group {}.\n\n\n\nHave questions? Simply reply to this email or visit our support site: http://support.suitabletech.com/\n\nYou can change your email notification settings here: {}/manage/#/account/notifications/\n\n\n\nThanks,\nSuitable Technologies\n\nSuitable Technologies, Inc.\n921 E Charleston Rd\nPalo Alto, CA 94303\n1-855-200-2326"
    # requires Organization Name, Organization Name, Device Group Name, ST URL
    
    AReservationForBeamWasCreateTitle = u"[Beam] A reservation for {} was created" #require beam name
    AReservationForBeamWasCreateContent = u""
    #require beam, user reserves, user is reserved for, start time, end time 
    
    AReservationIsRejectedTitle = u"[Beam] Your reservation for {} was rejected" #require beam name
    AReservationIsRejectedContent = u""
    #require beam, admin rejects, start time, end time 
    
    AReservationIsApprovedTitle = u"[Beam] You have a new reservation for {}" #require beam name
    AReservationIsApprovedContent = u""
    #require beam, admin approves, start time, end time 
    
    AReservationIsRemovedTitle = u"[Beam] Your reservation for {} was removed" #require beam name
    AReservationIsRemovedContent = u""
    #require beam, admin removes, start time, end time  
    
    InvitationEmailDeviceList_Single = u"You have access to the following Beam:"
    InvitationEmailDeviceList_Multiple = u"You have access to the following {} Beams:"
    
    RequestMessageLabel = u"Message:"
    
    TemporaryPassword = u""

    ActivityExportTitle = u"[Beam] Your activity export for LogiGear Test is ready for download"

    AReservationIsChangedTitle = u"[Beam] Your reservation for {} has changed" #require beam name
    AReservationIsChangedContent = u""
    #require beam, admin change, old start time, old end time, changed start time, change end time

    @staticmethod
    def initialize():
        #print("\n***\nApplicationConst::initialize()\n***\n")  
        EmailDetailConstants.WelcomeEmailTitle = _("WelcomeEmailTitle")
        EmailDetailConstants.WelcomeEmailContent = _("WelcomeEmailContent")
        EmailDetailConstants.DownloadInstallSoftwareLink = _("DownloadInstallSoftwareLink")
        EmailDetailConstants.WelcomeSimplifiedEmailContent = _("WelcomeSimplifiedEmailContent")
        EmailDetailConstants.ResentWelcomeSimplifiedEmailContent = _("ResentWelcomeSimplifiedEmailContent")
        EmailDetailConstants.WelcomeExistingEmailContent = _("WelcomeExistingEmailContent")
        EmailDetailConstants.WelcomeTemporaryUserEmailTitle = _("WelcomeTemporaryUserEmailTitle")
        EmailDetailConstants.WelcomeTemporaryUserEmailContent = _("WelcomeTemporaryUserEmailContent")
        EmailDetailConstants.WelcomeAdminCopyEmailTitle = _("WelcomeAdminCopyEmailTitle")
        EmailDetailConstants.WelcomeAdminCopyEmailContent = _("WelcomeAdminCopyEmailContent")
        EmailDetailConstants.BeamRequestAccessEmailTitle = _("BeamRequestAccessEmailTitle")
        EmailDetailConstants.BeamRequestAccessEmailContent = _("BeamRequestAccessEmailContent")
        EmailDetailConstants.AddedToDeviceGroupEmailTitle = _("AddedToDeviceGroupEmailTitle")
        EmailDetailConstants.AddedToDeviceGroupEmailContent = _("AddedToDeviceGroupEmailContent")
        EmailDetailConstants.RemovedFromDeviceGroupEmailTitle = _("RemovedFromDeviceGroupEmailTitle")
        EmailDetailConstants.RemovedFromDeviceGroupEmailContent = _("RemovedFromDeviceGroupEmailContent")
        EmailDetailConstants.ManageDeviceGroupEmailTitle = _("ManageDeviceGroupEmailTitle")
        EmailDetailConstants.ManageDeviceGroupEmailContent = _("ManageDeviceGroupEmailContent")
        EmailDetailConstants.RemovedFromOrgAdminEmailTitle = _("RemovedFromOrgAdminEmailTitle")
        EmailDetailConstants.RemovedFromOrgAdminEmailContent = _("RemovedFromOrgAdminEmailContent")
        EmailDetailConstants.AddedToOrgAdminEmailTitle = _("AddedToOrgAdminEmailTitle")
        EmailDetailConstants.AddedToOrgAdminEmailContent = _("AddedToOrgAdminEmailContent")
        EmailDetailConstants.TemporaryAccessTimeHasChangedTitle = _("TemporaryAccessTimeHasChangedTitle")
        EmailDetailConstants.TemporaryAccessTimeHasChangedContent = _("TemporaryAccessTimeHasChangedContent")
        EmailDetailConstants.BeamRemovedFromDeviceGroupTitle = _("BeamRemovedFromDeviceGroupTitle")
        EmailDetailConstants.BeamRemovedFromDeviceGroupContent = _("BeamRemovedFromDeviceGroupContent")
        EmailDetailConstants.AddToUserGroupEmailTitle = _("AddToUserGroupEmailTitle")
        EmailDetailConstants.AddToUserGroupEmailContent = _("AddToUserGroupEmailContent")
        EmailDetailConstants.PasswordChangedEmailTitle = _("PasswordChangedEmailTitle")
        EmailDetailConstants.PasswordChangedEmailContent = _("PasswordChangedEmailContent")
        EmailDetailConstants.PasswordResetEmailTitle = _("PasswordResetEmailTitle")
        EmailDetailConstants.PasswordResetEmailContent = _("PasswordResetEmailContent")
        EmailDetailConstants.CanNowAcceptSessionsEmailTitle = _("CanNowAcceptSessionsEmailTitle")
        EmailDetailConstants.CanNowAcceptSessionsEmailContent = _("CanNowAcceptSessionsEmailContent")
        EmailDetailConstants.CanNoLongerAcceptSessionsEmailTitle = _("CanNoLongerAcceptSessionsEmailTitle")
        EmailDetailConstants.CanNoLongerAcceptSessionsEmailContent = _("CanNoLongerAcceptSessionsEmailContent")
        EmailDetailConstants.GoogleChangeAuthEmailTitle = _("GoogleChangeAuthEmailTitle")
        EmailDetailConstants.GoogleChangeAuthEmailContent = _("GoogleChangeAuthEmailContent")
        EmailDetailConstants.GoogleChangeAuthEmailContant = _("GoogleChangeAuthEmailContant")
        EmailDetailConstants.NotificationAddedToDeviceGroupEmailTitle = _("NotificationAddedToDeviceGroupEmailTitle")
        EmailDetailConstants.NotificationAddedToDeviceGroupEmailContent = _("NotificationAddedToDeviceGroupEmailContent")
        
        EmailDetailConstants.GoogleChangeAuthConnectEmailContent = _("GoogleChangeAuthConnectEmailContent")
        EmailDetailConstants.DeleteDeviceGroupEmailTitle = _("DeleteDeviceGroupEmailTitle")
        EmailDetailConstants.DeleteDeviceGroupEmailContent = _("DeleteDeviceGroupEmailContent")
        EmailDetailConstants.InvitationEmailDeviceList_Single = _("InvitationEmailDeviceList_Single")
        EmailDetailConstants.InvitationEmailDeviceList_Multiple = _("InvitationEmailDeviceList_Multiple")
        EmailDetailConstants.RequestMessageLabel = _("RequestMessageLabel")
        EmailDetailConstants.TemporaryPassword = _("TemporaryPassword")
        EmailDetailConstants.ActivityExportTitle = _("ActivityExportTitle")
        EmailDetailConstants.AReservationForBeamWasCreateTitle = _("AReservationForBeamWasCreateTitle")
        EmailDetailConstants.AReservationForBeamWasCreateContent = _("AReservationForBeamWasCreateContent")
        EmailDetailConstants.AReservationIsRejectedTitle = _("AReservationIsRejectedTitle")
        EmailDetailConstants.AReservationIsRejectedContent = _("AReservationIsRejectedContent")
        EmailDetailConstants.AReservationIsApprovedTitle = _("AReservationIsApprovedTitle")
        EmailDetailConstants.AReservationIsApprovedContent = _("AReservationIsApprovedContent")
        EmailDetailConstants.AReservationIsRemovedTitle = _("AReservationIsRemovedTitle")
        EmailDetailConstants.AReservationIsRemovedContent = _("AReservationIsRemovedContent")
        EmailDetailConstants.AReservationIsChangedTitle = _("AReservationIsChangedTitle")
        EmailDetailConstants.AReservationIsChangedContent = _("AReservationIsChangedContent")
