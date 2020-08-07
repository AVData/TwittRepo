# Entry point for twitoff application
# in order to run application you must type the .py file in the terminal
# as such: FLASK_APP=twitoff:APP flask run

from .app import create_app

APP = create_app()
