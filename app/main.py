"""
Entry point for Cat or Dog - Simple ML application.
This application requires working Azure Function that works as ML Server.
"""
import logging
import os
from flask import Flask, render_template, request, redirect, session, url_for, abort
from models.ml_response import MLResponseClass
from helpers.file_cleanup import FileCleanup
from helpers.string_helpers import StringHelpers
from helpers.image_helpers import ImageHelpers

logging.basicConfig(filename=os.path.join('logs', 'application.log'), level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d : %(levelname)s : %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')

UPLOAD_FOLDER = 'static/resources/temp'
LOGS_FOLDER = 'logs'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

PROJECT_VERSION = '0.0.1'

APP = Flask(__name__)
APP.secret_key = b'crushyna'
APP.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
APP.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
APP.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', 'jpeg']
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """
    Function for checking, if uploaded file has correct extension.
    :param filename:
    """
    logging.info(f"Checking {filename} extension...")
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route("/hello")
def hello():
    """
    Test endpoint for application.
    :return: string
    """
    session['page_title'] = 'Hello!'
    return "Hello World from Flask in a uWSGI Nginx Docker " \
           "container with Python(from the example template)"


@APP.route("/")
def main():
    """
    Main route for the application. All wrong addresses are redirected here as well.
    """
    FileCleanup.file_cleanup(LOGS_FOLDER)
    session['page_title'] = 'Start'
    logging.info("Rendering welcome template.")
    return render_template("index.html")


@APP.route("/results")
def results():
    """
    Page displaying results of the Machine Learning
    """
    session['page_title'] = 'Results'
    FileCleanup.file_cleanup(UPLOAD_FOLDER)
    return render_template("results.html")


@APP.route("/", methods=['POST'])
def upload_file():
    """
    Upload file from the user to the web application.
    File gets checked, if it has correct extension.
    If yes, it gets resized for result page, and for ML engine (external).
    Than it's send to ML Server.
    Finally, function redirects to results page.
    :return: result page
    """
    session['filetype_ok'] = True  # assert as default value for modal message
    uploaded_file = request.files['image_file']
    if uploaded_file.filename != '':
        if not allowed_file(uploaded_file.filename):
            logging.info(f"Wrong file extension!")
            session['filetype_ok'] = False
            abort(502)

        logging.info(f"Correct file extension. Proceeding.")
        session['filetype_ok'] = True

        temp_filename = StringHelpers.generate_random_string(8)
        temp_filename_thumbnail = f"{temp_filename}_thumbnail.jpg"
        temp_filename_ml = f"{temp_filename}_ml.jpg"

        uploaded_file.save(os.path.join(UPLOAD_FOLDER, temp_filename))
        ImageHelpers.create_thumbnail(os.path.join(UPLOAD_FOLDER, temp_filename),
                                      os.path.join(UPLOAD_FOLDER, temp_filename_thumbnail))
        ImageHelpers.create_ml_image(os.path.join(UPLOAD_FOLDER, temp_filename),
                                     os.path.join(UPLOAD_FOLDER, temp_filename_ml))

        ml_response = MLResponseClass(os.path.join(UPLOAD_FOLDER, temp_filename_ml))

        session['ml_engine_result'] = ml_response.response['message']
        session['ml_engine_result_data'] = ml_response.response['data']
        session['ml_engine_result_status'] = ml_response.response['status']

        session['temp_filename'] = temp_filename
        session['temp_filename_thumbnail'] = temp_filename_thumbnail

    else:
        session['filetype_ok'] = False
        abort(502)

    return redirect(url_for('results'))


# ONLY Error handling below #
@APP.errorhandler(404)
def page_not_found(error):
    """
    Page not found handler.
    Redirects to starting page.
    :return: starting page
    """
    return render_template("index.html", error=error)


@APP.errorhandler(413)
def payload_too_large(error):
    """
    Payload too large handler.
    Redirects to error page with proper message.
    :return: error page with custom message
    """
    return render_template("error.html", error_message=f"File too large! Try again. {error}"), 413


@APP.errorhandler(502)
def bad_gateway(error):
    """
    Bad gateway handler.
    Occurs when file uploaded by user has improper type.
    Redirects to error page with proper message.
    :return: error page with custom message
    """
    return render_template("error.html", error_message=f"Wrong file type or file is missing. Images only! {error}"), 502


if __name__ == "__main__":
    # Only for debugging while developing
    APP.run(host="0.0.0.0", debug=True, port=80)
