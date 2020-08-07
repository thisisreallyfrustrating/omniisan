import os

from flask_minify import minify
from flask import Flask
import redis
from rq import Queue


# Change jinja default to %% as Vue uses {{
class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(variable_start_string="%%", variable_end_string="%%",))


app = CustomFlask(__name__)

app.config.from_object("omniisan.default_settings")
app.config.from_envvar("OMNIISAN_SETTINGS")

# minify assets
if not app.debug:
    minify(app=app, html=True, js=True, cssless=True)

# Redis/RQ
listen = ["default"]
redis_conn = redis.from_url(app.config["REDISTOGO_URL"])
redis_q = Queue(connection=redis_conn)

# Logging TODO
if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler

    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(
        os.path.join(app.config["LOG_DIR"], "omniisan.log"), "midnight"
    )
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter("<%(asctime)s> <%(levelname)s> %(message)s")
    )
    app.logger.addHandler(file_handler)

import omniisan.views  # noqa: F402,F401,E402
