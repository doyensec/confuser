from ast import parse
from crypt import methods
from struct import pack
from flask import Flask
from flask import render_template
from flask import request
import json
import npm

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    f = request.files['file']
    packages = npm.extract_packages(f)
    #return json.dumps(npm.get_vulnerable_packages(packages))
    return render_template("analyze.html", packages=npm.get_vulnerable_packages(packages))
