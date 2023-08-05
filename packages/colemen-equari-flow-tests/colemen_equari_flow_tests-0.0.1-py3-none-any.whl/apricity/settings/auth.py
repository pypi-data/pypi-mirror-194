
import os
import colemen_utils as _c



# ---------------------------------------------------------------------------- #
#                         AUTHORIZATION TOKEN SETTINGS                         #
# ---------------------------------------------------------------------------- #

# require_access_token_for_use:bool=True
# '''If False, all requests will be processed regardless of if a session with
# a validated access token has been created'''

cookie_name:str = "aesopian"
'''The name of the cookie in which the API access token can be stored.'''

access_token_expiration:int = 3600
'''How many seconds the access token is valid.\n
default: 3600'''

access_token_algo:str = "HS256"
'''The algorithm to use for generating the JWT signature.'''

access_token_secret:str = "w9v5K61EJbp8.RDa5GUuOBFbwJhHqX1z2Dep6tO0NJAspac2DxexJBIPH1u6k"
'''The token secret key used for encryption'''

access_token_value_length:int = 128
'''How long (in characters) the value stored in the JWT token & database should be'''



# ---------------------------------------------------------------------------- #
#                             BYPASS TOKEN SETTINGS                            #
# ---------------------------------------------------------------------------- #

bypass_token_cookie_name:str = "artuate"
'''The name of the cookie in which the API bypass token can be stored.'''

bypass_token_header_name:str = "mortala"
'''This is the name of the header in which the bypass token is stored'''

bypass_token_expiration:int = 3600
'''How many seconds the bypass token is valid.\n
default: 3600'''

bypass_token_algo:str = "HS256"
'''The algorithm to use for generating the JWT signature.'''

bypass_token_secret:str = "w9v5K61EJbp8.RDa5GUuOBFbwJhHqX1z2Dep6tO0NJAspac2DxexJBIPH1u6k"
'''The token secret key used for encryption,
This should ALWAYS be specified in the "prod_config.json" file.'''

bypass_token_value_length:int = 128
'''How long (in characters) the value stored in the JWT token & database should be'''



# ---------------------------------------------------------------------------- #
#                            INTERNAL CACHE SETTINGS                           #
# ---------------------------------------------------------------------------- #

cache_signature_salt:str = "CuajfQmtLWDyREb1aAKdZrLBHZ0GudUQazS8"
'''The salt used to generate cache file signatures.
This is not used for security stuff, so don't worry too much.'''



# ---------------------------------------------------------------------------- #
#                                REQUEST HEADERS                               #
#        The header settings used for altering the operation of server         #
# ---------------------------------------------------------------------------- #

test_mode_header:str = "apricity-test-mode"
'''The name of the header used to set test_mode to True'''

test_mode_header_value:str = "pFB7NkJblS5gub9DvrxEtc5zM7Y1AGJXgldacoP15gHWyLzk"
'''The value of the test_mode_header header used to set test_mode to True'''







management_creds:dict = {}
content_creds:dict = {}
meta_creds:dict = {}
business_creds:dict = {}

db_cache_path:str = f"{os.getcwd()}/db_cache"
'''The file path to where the database cache files should be saved.
Default: ./db_cache'''


# @Mstep [] check if the prod_config file exists in the current working directory.
if _c.file.exists("prod_config.json"):
    # @Mstep [] read the config file
    data = _c.file.read.as_json("prod_config.json")
    # @Mstep [if] if the config file is successfully read & parsed.
    if data is not False:
        _c.con.log("PRODUCTION CONFIGURATION LOCATED.","magenta")
        # @Mstep [LOOP] iterate the keys and values of the config.
        for k,v in data.items():
            # @Mstep [] update the settings with the config value.
            # if k in globals():
            globals()[k] = v
            # setattr(__name__,k,v)
            # k = v
            # print(f"    {k} = {v}")

