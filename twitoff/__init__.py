"""The following lines of code initialize the application.

Entry point for twitoff application.  In order to run application you must
type the following in the terminal: FLASK_APP=twitoff:APP flask run.
"""

from .app import create_app

APP = create_app()
