# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import








"""
    The Barn module containing the create_barn Route class declaration.

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 02-17-2023 08:11:55
    `version`: 1.0
    `module_name`: CreateBarn
    `member_of`: Barn
    * @xxx [02-17-2023 08:11:55]: documentation for CreateBarn
"""
import colemen_utils as c
import apricity.objects.Log as _log
import apricity.settings as _settings
from apricity.objects.Bases import RouteBase as _RouteBase


class RouteMain(_RouteBase):

    def __init__(self,Router:_settings.types.route_type) -> None:
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
        super().__init__(Router)
        self.name: str = None
        'The name of this route'
        self.activity_id: str = 'act_testRoute'
        'The id of the activity that this route performs'

    def master(self) -> None:
        """
            Execute the core functionality of this route.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-17-2023 08:11:55
            `version`: 1.0
            `method_name`: master
            * @xxx [02-17-2023 08:11:55]: documentation for master"""
        _log.add("TestRoute.Master","info")

    def execute(self) -> None:
        """
            This method executes the validations before attempting the master method.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 02-17-2023 08:11:55
            `version`: 1.0
            `method_name`: execute
            * @xxx [02-17-2023 08:11:55]: documentation for execute"""
        # @Mstep [IF] if the request is successfully validated.
        if self._validate():
            # @Mstep [] execute the master method of this route.
            self.master()
        else:
            _log.add("Request Failed Validation","error")

def main(Router:_settings.types.router_type) -> RouteMain:
    """
        Instantiate and execute an create_barn Route.:

        Return {RouteMain}
        ----------------------
        The create_barn route instance.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-17-2023 08:11:55
        `version`: 1.0
        `method_name`: main
        * @xxx [02-17-2023 08:11:55]: documentation for main"""
    _log.add('Create a TestRoute Instance',"info")
    route_instance = RouteMain(Router)
    route_instance.execute()
    return route_instance