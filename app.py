from http.client import OK
from pyexpat import model
from subprocess import call
from flask import Flask
from flask import render_template
from flask import request
import npm

from burp import BurpCollaboratorClient
import models

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
models.db.init_app(app)
with app.app_context():
    models.db.create_all()


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    f = request.files['file']
    packages = npm.extract_packages(f)
    # return json.dumps(npm.get_vulnerable_packages(packages))
    return render_template("analyze.html", packages=npm.get_vulnerable_packages(packages))


@app.route("/generate_poc")
def generate_poc():
    package_name = request.args.get('package')
    if not package_name:
        return "Provide package name.", 400

    npm.create_poc(package_name)
    return package_name


@app.route("/refresh")
def refresh():
    burp_client = BurpCollaboratorClient(
        "CslwqfTW39cQc7n+nuBgUaEYP9PEIOEuODuduIEoJIM=", "jylzi8mxby9i6hj8plrj0i6v9mff34")

    callbacks = burp_client.poll()
    for callback in callbacks:
        print(callback.get('data').keys())
        callback_record = models.Callback(protocol=callback.get("protocol", None), interactionString=callback.get("interactionString", None),
                                          time=callback.get("time"), client_ip=callback.get("client", None), request=callback.get("data").get("request", None),
                                          response=callback.get("data").get("response", None), subDomain=callback.get("data").get("subDomain", None))

        models.db.session.add(callback_record)
        models.db.session.commit()

    return "OK"
