


from typing import Literal


# ---------------------------------------------------------------------------- #
#                                 MODE SETTINGS                                #
#                                                                              #
#  These settings control the general "Mode" that the server is operating in.  #
# ---------------------------------------------------------------------------- #


mainentance_mode:bool=False
'''If True, all requests are denied unless the requestor has a
bypass header or cookie'''

coming_soon_mode:bool=False
'''If True, all requests are denied unless the requestor has a
bypass header or cookie'''

test_mode:bool=True
'''True if the server is operating in development mode and the
test header was provided.'''


# ---------------------------------------------------------------------------- #
#                               LOGGING SETTINGS                               #
# ---------------------------------------------------------------------------- #

log_to_console:bool=True
'''If True, all messages sent through the Log module are printed to the console'''

log_raise_error_exceptions:bool=True
'''If True, messages with a style that matches a built in exception name
will raise the exception.'''




# ---------------------------------------------------------------------------- #
#                               REQUEST SETTINGS                               #
# ---------------------------------------------------------------------------- #

literal_valid_request_methods=Literal["GET","POST","PATCH","PUT","DELETE","OPTIONS","HEAD"]
valid_request_methods:list = ["GET","POST","PATCH","PUT","DELETE","OPTIONS","HEAD"]
'''A list of valid request method names'''



# --------------------------- GET REQUEST LIMITING --------------------------- #
# ----------- These are the defaults used to control "GET" requests ---------- #

default_get_limit:int=100
'''The default number of rows that will can be returned when requesting
a data set. This is used primarily for paginating get results'''

get_limit_maximum:int=100
'''The maximum limit that a request is allowed to specify.'''

default_get_offset:int=0
'''The default offset to use for paginating get results.'''



# ---------------------------------------------------------------------------- #
#                            INTERNAL CACHE SETTINGS                           #
# ---------------------------------------------------------------------------- #

susurrus_cache_purge_lotto:int=2
'''An int from 1-100 representing the likelihood that the susurrus cache directory will be purged.'''



