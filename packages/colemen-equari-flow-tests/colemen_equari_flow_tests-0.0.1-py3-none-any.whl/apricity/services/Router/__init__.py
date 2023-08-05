# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    The router module creates the flask catch all route used for routing API requests.

    When flask executes this route, it will generate a Router instance and execute it's custom
    routing method.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 02-20-2023 08:14:12
    `name`: router
    * @xxx [02-20-2023 08:15:49]: documentation for router
'''




# import hashlib
# import importlib
# import json
# import re
from flask import Blueprint,request,make_response
import colemen_utils as c
import apricity.settings as _settings
import apricity.services.Router.Router as _router



router_blueprint = Blueprint('router_blueprint', __name__)



@router_blueprint.route("/",defaults={'path':''})
@router_blueprint.route('/<path:path>',methods=['POST','GET','DELETE'])
def master_router(path):
    rtr = _router.Router(path)
    rtr.master_routing()
    return rtr.response