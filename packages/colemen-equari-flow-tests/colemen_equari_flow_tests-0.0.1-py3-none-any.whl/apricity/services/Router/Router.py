# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import



from dataclasses import dataclass
import hashlib
import importlib
import json
import re
from flask import request,make_response
import colemen_utils as c
import apricity.settings as _settings
import apricity.objects.Result as _result
import apricity.objects.Url as _url
import apricity.objects.Log as _log


@dataclass
class Router:
    Url:_settings.types.url_type = None
    _request_data:dict = None
    '''A dictionary of data sent with the request.'''
    _ataraxia:str = None
    '''The ataraxia of the request'''
    # raw_url:str = None

    response = None
    '''The flask response instance.'''
    result:_settings.types.result_type = None
    '''The result object used for structured responses.'''
    route_data:dict = None
    '''A dictionary of data from the settings.routing module.'''

    def __init__(self,url:str) -> None:
        self.response = make_response()
        self.result = _result.Result()
        self.Url = _url.Url(url)
        self._request_data = data_to_dict(request.data)

    def master_routing(self):
        # TODO []: general blocking
        # TODO []: blackhole blocking
        # TODO []: authorization validation
        
        if self.get_by_ataraxia is False:
            _= self.get_by_url
        self._import_execute_route()
        
        
        
        # TODO []: request limiting
        self.response.set_data(self.result.json)

        return self.response


    def _validate(self):
        _log.add("Validating Request","info")
        self._is_test_mode()
        self.response.status_code = 200



        output = False
        # result = _result.Result()
        # xxx [12-23-2022 09:17:03]: general blocking validation
        # xxx [12-23-2022 11:03:15]: blackhole validation
        # TODO []: finish authorization
        # TODO []: create Reqeust limiter
        # TODO []: finish body,url,query data validations.
        validations = [
            "_general_blocking",
            "_blackhole",
            "_validate_authorization",
            # "_validate_method",
            # "_validate_data_provided",
            # "_validate_data_type",
            # "_validate_body",
            # "_validate_url_param_data",
        ]
        # if self.authorization_required is False or _settings.master_control.test_mode is True:
        #     validations.remove("_validate_authorization")

        _log.add("Validating Request","info")
        for valid in validations:
            valid_method = getattr(self, valid, None)
            if callable(valid_method):
                # pylint: disable=not-callable
                output = valid_method()
                if output is False:
                    _log.add(f"Failed: {valid}","warning")
                    break
                else:
                    _log.add(f"Passed Validation: {valid}","info")
        if output:
            _log.add("Successfully validated request",)
        return output






    def _import_execute_route(self):
        import_path = self.import_path
        if import_path is None:
            return False
        # @Mstep [] dynamically import the module.
        try:
            # module = importlib.import_module(import_path)
            module = importlib.import_module(import_path)
            module.main(self)
            self.response.status_code = 200
            self.result.set_key("route_data",self.route_data)
        except ModuleNotFoundError as e:
            print(f"e: {e}")


    @property
    def ataraxia(self):
        '''
            Get this Router's ataraxia

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-17-2023 10:43:29
            `@memberOf`: Router
            `@property`: ataraxia
        '''
        value = self._ataraxia
        if value is None:
            if "ataraxia" in self.request_data:
                value = self.request_data["ataraxia"]
                _log.add("Ataraxia found in request data.","info")
                self._ataraxia = value
            else:
                _log.add("Ataraxia not found in request data.","warning")
        return value

    @property
    def request_data(self):
        '''
            Get this Router's request_data

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-17-2023 10:46:20
            `@memberOf`: Router
            `@property`: request_data
        '''
        value = self._request_data
        return value

    @property
    def get_by_ataraxia(self):
        result = True
        ataraxia = self.ataraxia
        if isinstance(ataraxia,(str)) is False:
            return False
            # raise TypeError(f"The Ataraxia must be a string, received {type(ataraxia)}.")
        
        self.route_data = c.obj.get_arg(_settings.routing.ataraxia_lookup,[ataraxia],None,(dict))
        if self.route_data is None:
            c.con.log(f"Failed to lookup route using ataraxia:{ataraxia}","error")
            self.response.status_code = 404
            self.result.success = False
            _log.add("Failed to locate route with ataraxia","error")
            self.result.public_response = "Couldn't find route by ataraxia."
            result = False
        else:
            _log.add(f"Successfully located Route data with ataraxia: {ataraxia}","success")
        return result

    @property
    def get_by_url(self):
        '''
            Get this Router's get_by_url

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-17-2023 10:53:31
            `@memberOf`: Router
            `@property`: get_by_url
        '''
        value = None
        if self.Url.route_data is None:
            self.response.status_code = 404
            self.result.success = False
            _log.add("Failed to locate route with URL","error")
            self.result.public_response = "Couldn't find route by URL."
        else:
            self.route_data = self.Url.route_data
        return value

    @property
    def import_path(self):
        '''
            Get this Router's import_path

            `default`:None


            Meta
            ----------
            `@author`: Colemen Atwood
            `@created`: 02-17-2023 10:56:18
            `@memberOf`: Router
            `@property`: import_path
        '''
        value = None
        if self.route_data is not None:
            value = c.obj.get_arg(self.route_data,["import_path"],None,(str))
        return value





    # ---------------------------------------------------------------------------- #
    #                                  VALIDATIONS                                 #
    # ---------------------------------------------------------------------------- #



    def _is_test_mode(self):
        '''
            Determine if this route should be executed in test mode.

            Updates the global setting: `_settings.master_control.test_mode`

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-15-2022 08:34:41
            `memberOf`: __init__
            `version`: 1.0
            `method_name`: _is_test_mode
            * @xxx [12-15-2022 08:35:52]: documentation for _is_test_mode
        '''
        if request.root_url not in ['http://127.0.0.1:5000/']:
            _settings.master_control.test_mode = False
        else:
            header = request.headers.get(_settings.auth.test_mode_header,None)
            if header is not None:
                if header == _settings.auth.test_mode_header_value:
                    _settings.master_control.test_mode = True


    # def _general_blocking(self):
    #     '''
    #         This validation method is used to block requests when the server is in maintenance or coming soon mode.

    #         The coming soon mode can also be set on a specific route.

    #         If in either mode, the request can bypass this by providing the bypass header or cookie.

    #         ----------

    #         Return {bool}
    #         ----------------------
    #         True if the request is allowed to proceed, False otherwise.


    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-23-2022 09:11:54
    #         `memberOf`: __init__
    #         `version`: 1.0
    #         `method_name`: _general_blocking
    #         * @xxx [12-23-2022 09:14:02]: documentation for _general_blocking
    #     '''
    #     if self.coming_soon is False and _settings.master_control.coming_soon_mode is True:
    #         self.coming_soon = True

    #     if self.coming_soon is True or _settings.master_control.mainentance_mode is True:
    #         # @Mstep [] retrieve the bypass header
    #         result = _token.utils.get_bypass_token()
    #         # @Mstep [IF] if the token header is not found or fails validation.
    #         if result.success is False:
    #             # @Mstep [IF] if the reason was ["MISSING_BYPASS_HEADER","INVALID_BYPASS_TOKEN","EXPIRED_BYPASS_TOKEN"]
    #             if result.get_key("reason") in ["MISSING_BYPASS_HEADER","INVALID_BYPASS_TOKEN","EXPIRED_BYPASS_TOKEN"]:
    #                 # @Mstep [] set the response status_code to 503
    #                 self._response.status_code = 503
    #                 self.result.success = False
    #                 if self.coming_soon is True:
    #                     _log.add("   Coming soon mode is active, no bypass provided.")
    #                     self.result.public_response = "Coming Soon!"
    #                     self._response.headers.add_header("Retry-After",86400)
    #                 else:
    #                     _log.add("   Maintenance mode is active, no bypass provided.")
    #                     self.result.public_response = "We are working on some stuff, come back in a bit!"
    #                     self._response.headers.add_header("Retry-After",3600)
    #                 return False
    #         else:
    #             return True

    # def _blackhole(self):
    #     # TODO []: log activity showing further attempts to make requests after being blocked.
    #     ip_address = None
    #     if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
    #         ip_address = request.environ['REMOTE_ADDR']
    #     else:
    #         ip_address = request.environ['HTTP_X_FORWARDED_FOR']
    #     if ip_address is None:
    #         return True
    #     self.result.public_response = f"ip_address: {ip_address}"
    #     # _log.add(f"ip_address: {request.access_route[-1]}","info invert")
    #     from apricity.susurrus.Blackholes import Blackholes
    #     from apricity.objects.Blackhole import Blackhole as _Blackhole
    #     # @Mstep [] get all blackholes related to the ip_address
    #     result = Blackholes.get_blackholes({"ip_address":ip_address})
    #     # @Mstep [IF] if blackholes are found.
    #     if result is not None:
    #         if isinstance(result,_Blackhole) is False:
    #             return True
    #         _log.add("   Blackholes found for this client.","info")

    #         self.result.success = False
    #         black:_settings.types._blackhole_type = result
    #         # @Mstep [IF] if the blackhole is white listed
    #         if black.white_list is True:
    #             _log.add("   Client is whitelisted from blackholes","info")
    #             # @Mstep [RETURN] return True
    #             return True
    #         # @Mstep [] set the public response to the blackhole's message
    #         self.result.public_response = black.message

    #         # @Mstep [IF] if the reason is "BLACK_ROBOT"
    #         if black.reason in ["BLACK_ROBOT"]:
    #             _log.add("   Client is a BLACK_ROBOT and forbidden from requests.","info")
    #             # @Mstep [] set the status_code to 403
    #             self._response.status_code = 403

    #         # @Mstep [IF] if the reason is "TOO_MANY_REQUESTS"
    #         if black.reason in ["TOO_MANY_REQUESTS"]:
    #             _log.add("   Client has recently exceeded their request limits.","info")
    #             # @Mstep [] set the status_code to 429
    #             self._response.status_code = 429
    #             # @Mstep [IF] if the blackhole has an expiration timestamp
    #             if black.has_expiration is True:
    #                 # @Mstep [] set the "retry-after" header to the time delta.
    #                 self._response.headers.add_header("Retry-After",black.retry_after)


    #         # @Mstep [RETURN] return False
    #         return False
    #     _log.add("   no blackholes found for this client.","info")
    #     # @Mstep [RETURN] return True
    #     return True

    # def _validate_authorization(self):
    #     '''
    #         Retrieve the bearer token from the request and validate its value.
    #         ----------

    #         Return {bool}
    #         ----------------------
    #         True if the token is found and successfully validated,
    #         False otherwise.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 11-25-2022 08:22:37
    #         `memberOf`: __init__
    #         `version`: 1.0
    #         `method_name`: validate_authorization
    #         * @xxx [11-25-2022 08:23:33]: documentation for validate_authorization
    #     '''
    #     # @Mstep [IF] if authorization is not required or we are in test mode.
    #     if self.authorization_required is False or _settings.master_control.test_mode is True:
    #         _log.add("   Authorization is not required for this route.","info")
    #         # @Mstep [RETURN] return True.
    #         return True

    #     # @Mstep [] retrieve the bearer token from the request.
    #     result = _token.utils.get_bearer_token()
    #     # @Mstep [IF] if the token was not successfully retrieved
    #     if result.success is False:
    #         # @Mstep [] determine the reason for its failure.
    #         reason = result.get_key("reason")
    #         # @Mstep [IF] if the reason was ["MISSING_AUTH_HEADER","NON_BEARER_TOKEN","EXPIRED_ACCESS_TOKEN","INVALID_ACCESS_TOKEN",,"NO_TOKEN_IN_DATABASE"]
    #         if reason in ["MISSING_AUTH_HEADER","NON_BEARER_TOKEN","EXPIRED_ACCESS_TOKEN","INVALID_ACCESS_TOKEN","NO_TOKEN_IN_DATABASE"]:
    #             # @Mstep [] set the response status_code to 401
    #             # @Mstep [] This will let the frontend know that it needs to get authorization and try again.
    #             self._response.status_code = 401
    #             self.result.success = False
    #             self.result.public_response = "Nothing to see here"
    #             self._response.headers.add_header("WWW-Authenticate","Bearer")
    #             # @Mstep [RETURN] return False
    #             return False

    #     self.token = result.get_key("token")
    #     # @Mstep [RETURN] return True
    #     return True



def data_to_dict(data):
    result = None
    try:
        data = json.loads(data)
        result = data
    except json.JSONDecodeError:
        # self.response.status_code = 400
        # self.result.success = False
        # self.result.public_response = "These things you say make no sense."
        # return False
        result = False
    if isinstance(result,(dict)):
        nr = {}
        for k,v in result.items():
            if k.lower() in ["ataraxia"]:
                nr["ataraxia"] = v
                continue
            nr[c.string.to_snake_case(k.lower())] = v
        result = nr
    return result
