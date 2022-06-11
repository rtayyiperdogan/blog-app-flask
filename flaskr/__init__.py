import os
# 1. Create the application factory function.

# This class serves double duty. It will contain the application factory,
#  and it tells python that the flaskr directory should be treated as a package. 

from flask import Flask

#This is the application factory function.
# It is a function that takes a test_config argument, which is a dictionary of
# configuration values.
# If the test_config is not None, then the application is running tests and
# the test_config should be used.
# If the test_config is None, then the application is running normally and
# the config.py file should be used.

# The application factory function is used to create the application object.
# The application object is used to create the Flask application object.
# The Flask application object is used to create the Flask blueprint object.

def create_app(test_config = None):#Create the Flask instance

    # create and configure the app
    # The Flask application object is created here. this is the application object. It means app is the
    # application object. That means its instance of the Flask class.

    # __name__ is the name of the current Python module. If the module is being run directly,
    # __name__ is set to __main__. If the module is being imported, __name__ is set to the module's name.
    # The app needs to know where it's located to set up some paths, and __name__ is a convenient way to do that.

    # instance_relative_config=True tells the app that configuration file are relative to the instance folder.
    # The instance folder is located at out of the flaskr package and can hold local data that should not be
    # committed to version control, such as configuration data. Like database file. 
    app = Flask(__name__, instance_relative_config=True)
    #Set some default configuration that app will use:
    app.config.from_mapping(
        # SECRET_KEY is used by Flask and extensions to keep data safe.
        # It's set to 'dev' to provide a convenient value
        # during development, but it should be overridden with a random value in production/deploying.
        SECRET_KEY='dev',

        # DATABASE is the path to the database file.
        # This is the path where the SQLite database file will be saved. 
        # It's under app.instance_path, which is the path that Flask has chosen for instance folder.
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)#overrides the default configuration with values taken
        # from the config.py file in the instance folder if it exist!

        # For example, when deploying, this can be used to set a real SECRET_KEY.

    else:
        # load the test config if passed in
        
        app.config.from_mapping(test_config) # Sets some default configuration that the app will use.


    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)#Ensures that app.instance_path exists. Flask doesnt create the instance 
        # folder automatically, but it needs to be created because your project will craeate the SQLite database
        # file there.
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')#Creates a simple route. It creates a connection between the URL and the function.
    # URL is /hello. The function is hello() and a function that returns a response, the string 'Hello, World!'
    # in this case.
    def hello():
        return 'Hello, World!'


    from . import db
    db.init_app(app)

    return app