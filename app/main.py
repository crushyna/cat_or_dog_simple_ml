"""
Entry point for Cat or Dog - Simple ML application.
"""
import os
from time import sleep

from flask import Flask, render_template, request, redirect, session, abort, url_for

from app.helpers.file_cleanup import FileCleanup
from helpers.string_helpers import StringHelpers
from helpers.image_helpers import ImageHelpers

UPLOAD_FOLDER = 'static/resources/temp'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PROJECT_VERSION = '0.0.1'

APP = Flask(__name__)
APP.secret_key = b'crushyna'
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
APP.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']


@APP.route("/hello")
def hello():
    """
    Test endpoint for application.
    :return: string
    """
    return "Hello World from Flask in a uWSGI Nginx Docker container with Python 3.9.1 (from the example template)"


@APP.route("/")
def main():
    """
    Main route for the application. All wrong addresses are redirected here as well.
    """
    return render_template("index.html")


@APP.route("/results")
def results():
    """
    Page displaying results of the Machine Learning
    """
    FileCleanup.file_cleanup(UPLOAD_FOLDER)
    return render_template("results.html")


@APP.route("/", methods=['POST'])
def upload_file():
    uploaded_file = request.files['image_file']
    if uploaded_file.filename != '':
        file_ext = os.path.splitext(uploaded_file.filename)[1]
        if file_ext not in APP.config['UPLOAD_EXTENSIONS']:
            abort(400)  # TODO: add redirection to web page
        temp_filename = StringHelpers.generate_random_string(8)
        temp_filename_thumbnail = f"{temp_filename}_thumbnail.jpg"
        uploaded_file.save(os.path.join(UPLOAD_FOLDER, temp_filename))
        ImageHelpers.create_thumbnail(os.path.join(UPLOAD_FOLDER, temp_filename),
                                      os.path.join(UPLOAD_FOLDER, temp_filename_thumbnail))
        # create_ml_image(os.path.join(UPLOAD_FOLDER, temp_filename))
        session['temp_filename'] = temp_filename
        session['temp_filename_thumbnail'] = temp_filename_thumbnail
    return redirect(url_for('results'))


# TODO: Add redirect for 400 BAD_REQUEST


"""
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
"""

if __name__ == "__main__":
    # Only for debugging while developing
    APP.run(host="0.0.0.0", debug=True, port=80)
