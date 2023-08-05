"""
    Module containing the backend logging apparatus.

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 02-13-2023 14:03:19
    `version`: 1.0
    `module_name`: Log
    `member_of`: Log
    * @xxx [02-13-2023 14:03:19]: documentation for Log
"""

# pylint: disable=line-too-long
# pylint: disable=unused-import
# pylint: disable=import-outside-toplevel



import colemen_utils as c
import time
import json
from flask import request
import apricity.settings as _settings

LOG = []
DATA = {
    "log":[]
}

def result_array_logs()->list:
    '''
        Retrieve the current requests log array for the result object.
        If the server is NOT in test mode, this will always return an empty array.
        ----------

        Return {list}
        ----------------------
        A list of message logs.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-24-2023 10:06:52
        `version`: 1.0
        `method_name`: result_array_logs
        * @xxx [02-13-2023 14:02:19]: documentation for result_array_logs
    '''
    # @Mstep [IF] if the server is not in test mode.
    if _settings.master_control.test_mode is False:
        # @Mstep [RETURN] return an empty list.
        return []
    # @Mstep [ELSE] if the server is in test mode.
    else:
        # @Mstep [return] return the log array
        return LOG

def request_log()->str:
    '''
        Retrieve the current request log as a compressed base64 string.
        ----------

        Return {str}
        ----------------------
        The request log JSON as a compressed base64 string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-24-2023 10:02:54
        `version`: 1.0
        `method_name`: request_log
        * @TODO []: documentation for request_log
    '''
    import zlib
    import base64
    # text = b"Python Pool!" * 100
    bstring = bytes(json.dumps(LOG), 'utf-8')
    compressed = zlib.compress(bstring)
    print(f"compressed:{compressed}")

    # return str(compressed)
    return str(base64.b64encode(compressed))

def add(message,style="info"):
    '''
        Add a message to the current request log.
        ----------

        Arguments
        -------------------------
        `message` {any}
            The message of the log

        [`style`="info"] {str}
            The style or type of this log.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-24-2023 09:53:02
        `memberOf`: __init__
        `version`: 1.0
        `method_name`: add
        * @xxx [01-24-2023 09:54:09]: documentation for add
    '''
    data = {
        "timestamp":time.time(),
        "message":message,
    }

    LOG.append(data)
    if _settings.master_control.log_to_console is True:
        c.con.log(message,style)
    if _settings.master_control.log_raise_error_exceptions is True:
        if "error" in style:
            raise_exception(message,style)

def raise_exception(message:str,style:str):
    style = c.string.to_snake_case(style)
    if style in ["value_error"]:
        raise ValueError(message)
    if style in ["type_error"]:
        raise TypeError(message)
