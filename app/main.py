import os

from flask import Flask, send_file

APP = Flask(__name__)
PROJECT_VERSION = '0.0.1'


@APP.route("/hello")
def hello():
    return "Hello World from Flask in a uWSGI Nginx Docker container with Python 3.9.1 (from the example template)"


@APP.route("/")
def main():
    index_path = os.path.join(APP.static_folder, "index.html")
    return send_file(index_path)


# Everything not declared before (not a Flask route / API endpoint)...
@APP.route("/<path:path>")
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(APP.static_folder, path)
    if os.path.isfile(file_path):
        return send_file(file_path)
    # ...or should be handled by the SPA's "router" in front end
    index_path = os.path.join(APP.static_folder, "index.html")
    return send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    APP.run(host="0.0.0.0", debug=True, port=80)
