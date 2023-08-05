# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

from dataclasses import dataclass
import colemen_utils as c
import apricity.objects.Log as _log
import apricity.settings as _settings



@dataclass
class RouteBase:
    name:str = None
    
    '''The name of this route.'''
    response = None
    
    '''The flask response instance'''
    result:_settings.types.result_type = None

    activity_id:str = None
    '''The id of the activity that this route performs'''

    Router:_settings.types.router_type = None
    '''A reference to the master router instance.'''

    def __init__(self,Router:_settings.types.router_type) -> None:
        """
            The CreateBarn route class.
            Create a new barn

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-17-2023 08:11:55
            `version`: 1.0
            `method_name`: RouteMain
            * @xxx [02-17-2023 08:11:55]: documentation for RouteMain"""
        self.Router = Router
        self.response = Router.response
        self.result = Router.result

    def _validate(self):
        _log.add(f"{self.name}._validate","info")
        _log.add("Successfully Validated Request.","success")
        
        
        return True

