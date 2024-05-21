import os
from flask import Flask, render_template, request
from connector import Connector
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import importlib
import sys

version_util = importlib.import_module('lib-version.version_util')


template_dir = os.path.abspath('/app/app-frontend/templates')
app = Flask(__name__, template_folder=template_dir)

connector_to_model_service = Connector()

REQUEST_COUNT = Counter('page_requests', 'Number of requests to the page')

@app.route("/", methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        REQUEST_COUNT.inc()
        print(REQUEST_COUNT, file=sys.stderr)
        return render_template('index.html', version=version_util.VersionUtil.get_version())

    if request.method == 'POST':
        url = request.form['url_input']
        url_info = connector_to_model_service.get_url_data(url)
        return render_template('index.html', url_data=url_info["prediction"])

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

