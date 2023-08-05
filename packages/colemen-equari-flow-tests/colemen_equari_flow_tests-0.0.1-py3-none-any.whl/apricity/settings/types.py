




from typing import TypeVar as _TypeVar
from typing import TYPE_CHECKING

# from apricity.settings.apricity_types import *
# from dataclasses import dataclass, field
# from typing import List,Dict
# import modules.Log as _log

# from modules.ControlPanel import ControlPanel as _control_panel

INFLECT_ENGINE = None


_config = None
app_type = None
main_type = None
_database_type = None
result_type = None
url_type = None

column_type = None
router_type = None
route_type = None
_susurrus_base_type = None




if TYPE_CHECKING:
    from flask import Flask as _flask
    app_type = _TypeVar('app_type', bound=_flask)

    import apricity.objects.Result as _result
    result_type = _TypeVar('result_type', bound=_result.Result)

    # import apricity.objects.Column as _col
    # column_type = _TypeVar('column_type', bound=_col.Column)
    
    import apricity.services.Router.Router as _router
    router_type = _TypeVar('router_type', bound=_router.Router)

    import apricity.objects.Route as _route
    route_type = _TypeVar('route_type', bound=_route.Route)

    from apricity_labs import main as _main
    main_type = _TypeVar('main_type', bound=_main.Main)
    
    import apricity.objects.SusurrusBase as _sus_base
    _susurrus_base_type = _TypeVar('_susurrus_base_type', bound=_sus_base.SusurrusBase)
    
    import apricity.objects.Url as _url
    url_type = _TypeVar('url_type', bound=_url.Url)
    



# def is_entity(obj)->bool:
#     '''
#         Determine if the object provided is an apricity entity (object).
#         ----------

#         Arguments
#         -------------------------
#         `obj` {any}
#             The object to test.

#         Return {bool}
#         ----------------------
#         True if the object is an apricity entity, False otherwise.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 01-24-2023 10:20:02
#         `version`: 1.0
#         `method_name`: is_entity
#         * @xxx [01-24-2023 10:20:58]: documentation for is_entity
#     '''
#     from apricity.objects.Bases.EntityBase import EntityBase as _ebase
#     if isinstance(obj,_ebase):
#         return True
#     return False


