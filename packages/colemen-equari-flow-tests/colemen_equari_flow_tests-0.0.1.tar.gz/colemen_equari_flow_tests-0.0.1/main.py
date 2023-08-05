# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
import os


# import colemen_utils as c

from flask import Flask,Blueprint
import apricity.services.Router as _router





class Main:
    '''
        The wrapping class for control the setup of the Flask instance and its routes.

        ----------


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-02-2022 08:11:08
        `memberOf`: apricity_labs
        `version`: 1.0
        `method_name`: Main
        * @TODO []: documentation for Main
    '''
    force_run:bool = False
    '''
        If True the development server will be ran\n
        If this is done on the production server, it will throw a fatal error.
    '''

    app:Flask = None
    '''The Flask application instance'''

    def __init__(self):
        self.settings = {}
        self.data = {}
        self.force_run = False
        self.app = Flask(__name__)

    def prep(self):
        '''
            Iterate all known service blueprints and register them with the master blueprint.
            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 01-24-2023 10:13:56
            `memberOf`: apricity_labs
            `version`: 1.0
            `method_name`: prep
            * @xxx [01-24-2023 10:14:54]: documentation for prep
        '''
        # @Mstep [] instantiate the master blueprint.
        master_blueprint = Blueprint('master_blueprint', __name__)


        # @Mstep [] register the blueprint with the master blueprint.
        master_blueprint.register_blueprint(_router.router_blueprint)

        # @Mstep [] finally, register the master blueprint with flask.
        self.app.register_blueprint(master_blueprint)

    # def set_defaults(self):
        # self.settings = c.file.import_project_settings("__TITLE__.settings.json")

    def start(self):
        print("master")
        self.prep()
        # @Mstep [IF] if this is the main file.
        # This is necessary for use with pythonanywhere, otherwise it will cause a fatal error.
        if __name__ == '__main__' or self.force_run:
            # @Mstep [] run the development server.
            self.app.debug = True
            self.app.run()



# ------------------------- INSTANTIATE MAIN INSTANCE ------------------------ #
main = Main()
# MAIN.log = a.objects.Log.Log()
# main = main
# LOG = main.log

# ----------------------------- IMPORT ALL ROUTES ---------------------------- #


from apricity import *
# from globe import OMNI as o
# import apricity.services.home.routes as _home
# import apricity.services as _services

# import apricity.services.account.routes as _acc
# import services.auth.routes as _auth





def start():
    main.start()








if __name__ == '__main__':
    main.start()

