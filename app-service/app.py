import os
from flask import Flask, render_template, request
from connector import Connector
import importlib

version_util = importlib.import_module('lib-version.version_util')


template_dir = os.path.abspath('/app/app-frontend/templates')
app = Flask(__name__, template_folder=template_dir)

connector_to_model_service = Connector()

@app.route("/", methods = ['GET', 'POST'])
def index():
    print("hey", request.method)
    if request.method == 'GET':
        return render_template('index.html', version=version_util.VersionUtil.get_version())

    if request.method == 'POST':
        url = request.form['url_input']
        url_info = connector_to_model_service.get_url_data(url)
        return render_template('index.html', url_data=url_info["prediction"])
