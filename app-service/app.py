import os
from flask import Flask, render_template, request
from connector import Connector
from prometheus_client import Counter, Gauge, Summary, Histogram, generate_latest, CONTENT_TYPE_LATEST
import importlib
import sys

version_util = importlib.import_module('lib-version.version_util')


template_dir = os.path.abspath('/app/app-frontend/templates')
app = Flask(__name__, template_folder=template_dir)

connector_to_model_service = Connector()

PAGE_REQUEST_COUNT = Counter('page_requests', 'Number of requests to the page')
MODEL_REQUEST_COUNT = Counter('model_requests', 'Number of requests to the model')
PHISHING_COUNT = Counter('phishing_detection', 'The number of URLs detected as phishing')
USER_PHISHING_GUESS_COUNT = Counter('user_phishing_guess', 'Number of phishing guesses for a user')
USER_SAME_GUESS_COUNT = Counter('user_same_guess', 'Number of guesses for a user that agree with model')
USER_GUESS_AGREE_GAUGE = Gauge('user_guess_status', '1 if user agrees with the model in their newest phishing or not guess, 0 otherwise')
PHISHING_RATE = Gauge('phishing_rate', 'The percentage of URLs detected as phishing out of the total URLs checked')
USER_PHISHING_GUESS_RATE = Gauge('user_phishing_guess_rate', 'The percentage of guesses that are phishing')
USER_SAME_GUESS_RATE = Gauge('user_same_guess_rate', 'The percentage of guesses in agreement with the model')
MODEL_REQUEST_SUMMARY = Summary('model_request_summary', 'Summary of the model request durations')
MODEL_REQUEST_HISTOGRAM = Histogram('model_request_histogram', 'Histogram of the model request durations')


@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        PAGE_REQUEST_COUNT.inc()
        print(PAGE_REQUEST_COUNT, file=sys.stderr)
        return render_template('index.html', version=version_util.VersionUtil.get_version())

    if request.method == 'POST':
        with MODEL_REQUEST_SUMMARY.time():
            with MODEL_REQUEST_HISTOGRAM.time():
                url = request.form['url_input']
                MODEL_REQUEST_COUNT.inc()

                if 'yesButton' in request.form:
                    # User thinks it's phishing
                    user_thinks_phishing = True
                    USER_PHISHING_GUESS_COUNT.inc()
                elif 'noButton' in request.form:
                    # User thinks it's innocent
                    user_thinks_phishing = False

                url_info = connector_to_model_service.get_url_data(url)

                if url_info["prediction"] == "phishing":
                    PHISHING_COUNT.inc()
                    if user_thinks_phishing:
                        # User guessed the same as model
                        USER_SAME_GUESS_COUNT.inc()
                        USER_GUESS_AGREE_GAUGE.set(1)
                    else:
                        # User did not
                        USER_GUESS_AGREE_GAUGE.set(0)
                elif url_info["prediction"] == "legitimate":
                    if not user_thinks_phishing:
                        # User guessed the same as model
                        USER_SAME_GUESS_COUNT.inc()
                        USER_GUESS_AGREE_GAUGE.set(1)
                    else:
                        # User did not
                        USER_GUESS_AGREE_GAUGE.set(0)
                model_request_count = MODEL_REQUEST_COUNT._value.get()
                if model_request_count > 0:
                    PHISHING_RATE.set((PHISHING_COUNT._value.get() / model_request_count) * 100)
                    USER_PHISHING_GUESS_RATE.set((USER_PHISHING_GUESS_COUNT._value.get() / model_request_count) * 100)
                    USER_SAME_GUESS_RATE.set((USER_SAME_GUESS_COUNT._value.get() / model_request_count) * 100)
                return render_template('index.html', url_data=url_info["prediction"])

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

