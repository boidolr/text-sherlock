# http://werkzeug.pocoo.org/docs/serving/#werkzeug.serving.run_simple
from core import flask
from core import settings as core_settings
import webapp.settings

app = flask.Flask('webapp')
app.config.from_object('webapp.settings')

from . import views

# The number of processes to spawn for the server.
# You can only have one or the other; multi-threaded or multi-process.
# Only applies to the default server, non-DEBUG mode.
# type: integer
# default: 1
SERVER_PROCESSES = 1

# True if the web server process should handle each request in a separate thread.
# You can only have one or the other; multi-threaded or multi-process.
# Only applies to the default server, non-DEBUG mode.
# type: boolean
# default: True
SERVER_IS_THREADED = True


def get_server_type():
    stype = core_settings.SERVER_TYPE
    if not stype or stype == 'default':
        return 'werkzeug (default)'
    return stype


def run():
    """Runs the flask app server
    """
    server_type = core_settings.SERVER_TYPE
    if server_type == 'cherrypy':
        # near-production level server (small to medium traffic)
        from . import server_cherrypy
        server_cherrypy.run()
    else:  # default server (flask/werkzeug)
        if SERVER_PROCESSES > 1 and SERVER_IS_THREADED:
            raise Exception('Choose either multi-threaded or multi-process')
        # dev or low traffic
        app.run(
            host=core_settings.SERVER_ADDRESS,
            port=core_settings.SERVER_PORT,
            debug=core_settings.DEBUG,
            # support multi-thread requests outside of DEBUG mode
            threaded=SERVER_IS_THREADED,
            processes=SERVER_PROCESSES
        )
