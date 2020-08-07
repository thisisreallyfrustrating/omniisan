import requests

from omniisan import app


RECAPATCHA_SECRET_KEY = app.config["RECAPATCHA_SECRET_KEY"]


def validate_recaptcha(client_response):
    response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        params={"secret": RECAPATCHA_SECRET_KEY, "response": client_response},
    )
    if response.json()["success"]:
        return True
