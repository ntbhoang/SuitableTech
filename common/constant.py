# -*- coding: utf-8 -*-
class Browser(object):
    Firefox = "Firefox"
    IE = "IE"
    Chrome = "Chrome"
    Safari = "Safari"
    Edge = "Edge"


class Platform(object):
    WINDOWS = "WINDOWS"
    MAC = "MAC"
    ANDROID = "ANDROID"
    IOS = "IOS"
    ANY = "ANY"


class Language(object):
    ENGLISH = "ENGLISH"
    JAPANESE = "JAPANESE"
    FRENCH = "FRENCH"


class Locale(object):
    US = "US"
    FR = "FR"


class Remote_Type(object):
    GRID = "GRID"
    SAUCELABS = "SAUCELABS"
    BROWSERSTACK = "BROWSERSTACK"
    

class Constant(object):
    import os
    
    LGGDomain = "logigear.com"
    SauceLabs = "SAUCELABS"
    RunEnvironmentFile = "data_test/RunEnv.txt"
    DevicePool = "Devices POOL"
    SuitableTechURL = "https://stg1.suitabletech.com"
    SuitableTechHomeURL = SuitableTechURL + "/manage/{}/#/home/"
    SuitableTechWelcomeURL = SuitableTechURL + "/welcome/"
    SuitableTechLoginURL = SuitableTechURL + "/accounts/login/"
    SuitableTechLogoutURL = SuitableTechURL + "/accounts/logout/"
    GoogleSignInURL = "https://accounts.google.com/ServiceLogin"
    GoogleSignUpURL = "https://accounts.google.com/SignUp"
    AppsConnectedURL = "https://security.google.com/settings/u/7/security/permissions?pli=1"
    OktaAccountURL = "https://dev-463039.oktapreview.com/"
    DownloadBeamAppURL = "https://stg1.suitabletech.com/installers/stable"
    LinkABeamURL = "https://stg1.suitabletech.com/setup/link/?o={}"
    HelpCenterURL = "https://www.suitabletech.com/support/helpcenter"
    
    SimplifiedAdminEmail = os.environ['SimplifiedAdminEmail']
    AdvanceOrgAdminEmail = os.environ['AdvanceOrgAdminEmail']
    MixedMultiOrgAdminEmail = os.environ['MixedMultiOrgAdminEmail']
    OktaAccount = os.environ['OktaAccount']
    OktaPassword = os.environ['OktaPassword']
    OneLoginAccount = os.environ['OneLoginAccount']
    OneLoginPassword = os.environ['OneLoginPassword']
    DefaultPassword = os.environ['DefaultPassword']
    AllowedGSSOEmails = os.environ['AllowedGSSOEmails']
    UnallowedGSSOEmails = os.environ['UnallowedGSSOEmails']
    AdvanceDeviceGroupAdmin = os.environ['AdvanceDeviceGroupAdminEmail']
    
    BaseEmail_1 = os.environ['BaseEmail_1']
    BaseEmail_2 = os.environ['BaseEmail_2']
    BaseEmail_3 = os.environ['BaseEmail_3']
    BaseEmail_4 = os.environ['BaseEmail_4']
    BaseEmail_5 = os.environ['BaseEmail_5']
    
    BaseEmails = { 1: BaseEmail_1, 2: BaseEmail_2, 3: BaseEmail_3, 4: BaseEmail_4, 5: BaseEmail_5 }
    
    # Info to create a new GG account
    GGAccFirstName = "lgvn"
    GGAccLastName = "suitabletech"
    GGAccMonth = "January"
    GGAccGender = "Female"
    
    # Organization Names
    AdvancedOrgName = "LogiGear Test"  # includes AdvancedAdmin Admin
    SimplifiedOrgName = "LogiGear Test 2"  # includes SimpleAdmin Admin
    AdvancedOrgName_2 = "LogiGear Test 3"  # includes AdvancedAdmin and AdvancedMultiOrg Admins
    OktaOrgName = "LogiGear Okta" # includes Okta Admin
    OneLoginOrgName = "LogiGear Onelogin" # includes Okta Admin

    OrgName = { 1:"LogiGear Test", 2:"LogiGear Test 2", 3:"LogiGear Test 3"}

    # Beam Names
    BeamPlusName = u"QA BeamPlus Visitor1"
    BeamProNameUTF8 = u"QA BeamPro \u00a9 Visitor1"  # QA BeamPro © Visitor1
    BeamPlusMock1Name = u"LogiGear Mock Beam+ 1"
    BeamPlusMock2Name = u"LogiGear Mock Beam+ 2"
    BeamPlusMock3Name = u"LogiGear Mock Beam+ 3"
    BeamPlusMock4Name = u"LogiGear Mock Beam+ 4"
    BeamPlusMock5Name = u"LogiGear Mock Beam+ 5"
    BeamPlusMock6Name = u"LogiGear Mock Beam+ 6"
    BeamPlusMock2ID = u"860"
    BeamPlusMock3ID = u"861"
    
    # API Section
    APIBaseURL = "https://stg1.suitabletech.com/admin-api/2/organizations/{}/"
    APIKeys = {'LogiGear Test':'APIKEY:8Qfu4d1B5q/N:/cgxlSN7v3ThyzI5ARiVnWBSuImuMTrn7kPqM1TbES9y',
               'LogiGear Test 3':'APIKEY:BwTeIJ4EUG05:ULJGvbqjbjQF6Pl1vqJreOpP3zLsQFDQ6K8Gl0K0rMBG',
               'LogiGear Okta' : 'APIKEY:ePuiB1gqPMLj:ZoDBfqbE2Vqvjv4TumqLzG/oql9HwmQ5OS7DKH2dPwbf'}
    SauceLabsAuth = {'User':'logigear04042017','Access Key':'8f498456-714f-4775-89b4-f9de86ee175e'}
    DeviceIDs = {'LogiGear Mock Beam+ 1':'logigear-mock-beamplus-1', 
                 'LogiGear Mock Beam+ 4':'logigear-mock-beamplus-4',
                 'LogiGear Mock Beam+ 5':'logigear-mock-beamplus-5', 
                 'LogiGear Mock Beam+ 6':'logigear-mock-beamplus-6',
                 'QA BeamPlus Visitor1':'beam135909030', 
                 'QA BeamPro © Visitor1':'beam100108146',
                 'LogiGear Mock Beam+ 2':'860', 
                 'LogiGear Mock Beam+ 3':'861',
                 'LogiGear Mock Beam+ 7': '20116', 
                 'LogiGear Mock Beam+ 8': '20118'}
    
    OrgsInfo = {'LogiGear Test': '129', 'LogiGear Test 2': '130', 'LogiGear Test 3': '131', 'LogiGear Okta': '143', 'LogiGear Onelogin': '144' }
    
    AdvancedBeams = [{"name": u"QA BeamPlus Visitor1", "id": "beam135909030", "organization": "LogiGear Test"},
                     {"name": u"QA BeamPro \u00a9 Visitor1", "id": "beam100108146", "organization": "LogiGear Test"},
                     {"name": u"LogiGear Mock Beam+ 1", "id": "logigear-mock-beamplus-1", "organization": "LogiGear Test"},
                     {"name": u"LogiGear Mock Beam+ 4", "id": "logigear-mock-beamplus-4", "organization": "LogiGear Test"},
                     {"name": u"LogiGear Mock Beam+ 5", "id": "logigear-mock-beamplus-5", "organization": "LogiGear Test"},
                     {"name": u"LogiGear Mock Beam+ 6", "id": "logigear-mock-beamplus-6", "organization": "LogiGear Test"}]
    
    SimplifiedBeams = [{"name": u"LogiGear Mock Beam+ 2", "id": "860", "organization": "LogiGear Test 2"},
                       {"name": u"LogiGear Mock Beam+ 3", "id": "861", "organization": "LogiGear Test 2"},
                       {"name": u"LogiGear Mock Beam+ 7", "id": "20116", "organization": "LogiGear Test 2"},
                       {"name": u"LogiGear Mock Beam+ 8", "id": "20118", "organization": "LogiGear Test 2"}]
    
    #Info to configure auth methods (OneLogin, Okta)
    OneloginAppid = "576864"
    OneloginSubdomain = "staging-suitabletech-dev"
    OneloginFingerprint = "E1:77:F7:EB:6C:F3:53:60:AB:7D:F3:7D:11:39:36:34:93:44:41:7D"
    idp = {'onelogin':'onelogin','okta':'okta'}
    OneloginCertificate = """
    -----BEGIN CERTIFICATE-----
    MIIEPjCCAyagAwIBAgIUWSwfzB5bzWPqmieBYKnSZTXLcQIwDQYJKoZIhvcNAQEF
    BQAwZTELMAkGA1UEBhMCVVMxHjAcBgNVBAoMFVN1aXRhYmxlIFRlY2hub2xvZ2ll
    czEVMBMGA1UECwwMT25lTG9naW4gSWRQMR8wHQYDVQQDDBZPbmVMb2dpbiBBY2Nv
    dW50IDg5NzUxMB4XDTE2MDgxNTE2MzczOFoXDTIxMDgxNjE2MzczOFowZTELMAkG
    A1UEBhMCVVMxHjAcBgNVBAoMFVN1aXRhYmxlIFRlY2hub2xvZ2llczEVMBMGA1UE
    CwwMT25lTG9naW4gSWRQMR8wHQYDVQQDDBZPbmVMb2dpbiBBY2NvdW50IDg5NzUx
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwe/YUUcqxfwcPjHXvYsg
    JJzrMv+521P15dRDQ2FqEmZXl1lCXjROXpumqOsagaeCWpG3ytbpbTFJsIBFF+Gy
    JsYEjBfMsSfbPxWGh3wMwLMgFEuAIp1fBEZj5almMziKDFxzy2vBCQ2cjNgmLrBE
    of2VluwV0NlXeO4Vyqp6ThKXPFeu97aUFcNTwuTOmHIfuNWd6v7Dw0vzjZlHYOmB
    RvY5oGYsbWk3EJqmaGDcLmATQEwaJDah9unXGGyYBJlmaV8Nk94q5n5YQk+603qJ
    LO3qUQ8q/Dl5PFi6PdPtQz6k57/QfAiVZE3nglug+Q0NOC1c7I5M9LI1wjvFdnWy
    bQIDAQABo4HlMIHiMAwGA1UdEwEB/wQCMAAwHQYDVR0OBBYEFKvEo7JfNIpk9FuR
    gva7Nv2lt+iGMIGiBgNVHSMEgZowgZeAFKvEo7JfNIpk9FuRgva7Nv2lt+iGoWmk
    ZzBlMQswCQYDVQQGEwJVUzEeMBwGA1UECgwVU3VpdGFibGUgVGVjaG5vbG9naWVz
    MRUwEwYDVQQLDAxPbmVMb2dpbiBJZFAxHzAdBgNVBAMMFk9uZUxvZ2luIEFjY291
    bnQgODk3NTGCFFksH8weW81j6pongWCp0mU1y3ECMA4GA1UdDwEB/wQEAwIHgDAN
    BgkqhkiG9w0BAQUFAAOCAQEAuBkqxQZeVsk+5GGhwDHj5f4JnwFUaj6q/N9irPSm
    m0zFMHbX5F2S9L+NlScK402AzsAuagv0Vpr8GvehG+BaHBUYfU/E5DbPrRcTxJpt
    vNrSfBszhu1j4K5GkygO7NDTLPbYKuKk1b/YcidLoGJBVVnac2xQB0IPToJvFJgD
    yQCv2h1H+7xsEoFxSVLzk5hOpRwCDnxxvMwGu0Hy6jVEETb0YFfGmLvgLdWP4Xvs
    C+7URHYEwhgDIHCt7yTN9iUjkF7ksnV8GFXVC45JuYrZnod9Cva53oPLiG3oMC4G
    i/WgpCjpIcqWzWyVnPZMgwBjAb7PXGT11C36tKrCMEvSQw==
    -----END CERTIFICATE-----"""

    # Credit Card Info
    AmericanExpress = {'number':'371449635398431', 'name':'american express', 'exp_month':'8', 'exp_year':'2020', 'security_code':'8888', 'brand':'American Express'}
    Discover = {'number':'6011111111111117', 'name':'discover', 'exp_month':'9', 'exp_year':'2021', 'security_code':'9999', 'brand':'Discover'}

    # App string
    DefaultMessage = 'Hello'

    # Privileges icon
    IconName = {'org_admin':'is_admin', 'guest_user':'is_guest', 'temp_user':'is_temporary'}

    #Primary Contact
    PrimaryContactDefaultInfo = {
                                    "contact_info": {
                                        "last_name": "Le",
                                        "phone": "+8499999999",
                                        "postal_code": "55000",
                                        "city": "Ho Chi Minh",
                                        "first_name": "Tan",
                                        "country": "Viet Nam",
                                        "state": "Phu Nhan",
                                        "company_name": "Logigear",
                                        "job_title": "Testing",
                                        "address_line_2": "",
                                        "email": "tan.minh.le@logigear.com",
                                        "address_line_1": "Viet Nam"
                                    }
                                }
