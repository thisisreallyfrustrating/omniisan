import schema
from flask_restful import Resource, Api
from flask import request, send_from_directory, render_template, jsonify, make_response
from rq.job import Job as RQJob
from rq.exceptions import NoSuchJobError
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from omniisan import app, redis_q, redis_conn
from omniisan.schemas import TASK
from omniisan.util import validate_recaptcha
from omniisan.wrapsfff import download  # noqa: F401


api = Api(app)
limiter = Limiter(app, key_func=get_remote_address)


@app.route("/static/<path:path>")
def send_static(path):
    """
    Route static assets such as js.

    Minified if running in production.
    """
    return send_from_directory("static", path)


@app.route("/")
def root():
    """"
    index.html pulls some values from app.config and must be rendered
    as a template
    """
    return render_template("index.html")


class Job(Resource):
    decorators = [limiter.limit("5/hour")]

    def post(self):
        """"
        Adds ebook tasks to queue.

        POST http://localhost:5000/jobs
        Content-Type: application/json

        {"url": "https://forums.spacebattles.com/threads/...",
        "g-recaptcha-response": "..."}
        """

        try:
            data = TASK.validate(request.json)
        except schema.SchemaMissingKeyError:
            return {"message": "Missing fields in your api request."}, 400
        except schema.SchemaError:
            return {"message": "This looks like a bad url to me."}, 400
        if not validate_recaptcha(data["g-recaptcha-response"]):
            return {"message": "Request failed to pass recaptcha."}, 400
        queue_length = len(redis_q)
        if queue_length >= 5:
            return (
                {
                    "message": f"The queue is full with {queue_length} items. Try again in a minute."
                },
                400,
            )
        # line needed for rq
        from omniisan.wrapsfff import download  # noqa: F811

        job = redis_q.enqueue_call(
            func=download,
            args=(
                data["url"],
                app.config["OUTPUT_PATH"],
                app.config["PATH_TO_FANFICFARE"],
            ),
            timeout=180,
            result_ttl=5000,
        )
        return (
            {
                "message": "Request accepted by server.",
                "task_url": f"/jobs/{job.get_id()}",
            },
            201,
        )


class JobState(Resource):
    def get(self, job_id):
        """
        Monitor queue for status. Return story url on success.

        GET http://127.0.0.1:5000/jobs/bfde3151-855d-4c52-b5a3-c9420039bf0e
        """
        try:
            job = RQJob.fetch(job_id, connection=redis_conn)
        except NoSuchJobError:
            return {"message": "Job does not exist!"}, 404
        if job.is_finished:
            success, result = job.result
            if success:
                return (
                    {
                        "done": True,
                        "message": "Ebook ready for consumption.",
                        "link": f"/stories/{result}",
                    },
                    200,
                )
                # TODO queue deletion task
            else:
                return {"done": True, "message": "Download failed.\n"}, 400
        else:
            if job.is_started:
                return {"done": False, "message": "Working on it. Hang in there."}
            else:
                return {"done": False, "message": "Waiting your turn in the queue."}


class Story(Resource):
    def get(self, story_name):
        return send_from_directory("../stories", story_name)  # TODO value from config


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(
        jsonify(
            message="Omniisan has a request limit of 5 stories per hour. Try again later."
            % e.description
        ),
        429,
    )


api.add_resource(Job, "/jobs")
api.add_resource(JobState, "/jobs/<job_id>")
api.add_resource(Story, "/stories/<story_name>")
