import datetime
import json
import regex
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from itsdangerous import base64_decode
import npm

from burp import BurpCollaboratorClient
import models

json_pattern = r'\{(?:[^{}]|(?R))*\}'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///confuser.db'
models.db.init_app(app)
with app.app_context():
    models.db.create_all()

@app.template_filter('datetime')
def format_date(epoch):
    return datetime.datetime.fromtimestamp(epoch/1000.0).strftime("%m/%d/%Y, %H:%M:%S")

@app.route("/")
def main():
    projects = models.Project.query.all()

    return render_template("main.html", projects=projects)


@app.route("/project/<project_id>")
def project(project_id):
    project = models.Project.query.get(project_id)
    if not project:
        return "", 404

    vulnerable_dependencies = project.packages.filter_by(vulnerable=True).all()
    callbacks = project.callbacks.order_by(models.Callback.time.asc()).all()

    return render_template("project.html", project=project, packages=vulnerable_dependencies, callbacks=callbacks)


@app.route("/project/create", methods=["POST"])
def analyze():
    f = request.files['file']
    package = npm.parse_package(f)
    project_record = models.Project(package.get("name", ""), "")
    dependencies = package.get("dependencies")
    vulnerable_dependencies = npm.get_vulnerable_packages(dependencies)
    vulnerable_dependencies = list(vulnerable_dependencies)
    for dependency in dependencies.keys():
        print(type(dependency))
        package_record = models.Package(dependency, dependencies.get(
            dependency), dependency in vulnerable_dependencies)
        project_record.packages.append(package_record)

    models.db.session.add(project_record)
    models.db.session.commit()
    models.db.session.refresh(project_record)
    # return json.dumps(npm.get_vulnerable_packages(packages))
    return redirect("/project/{}".format(project_record.id))

@app.route("/project/start_campaign", methods=["POST"])
def start_campaign():
    project_id = request.form["project_id"]
    package_id = request.form["package_id"]

    package = models.Package.query.get(package_id)
    npm.generate_package(project_id, package, True)
    package.campaign_active=True
    models.db.session.commit()
    return redirect("/project/{}".format(project_id))

@app.route("/project/stop_campaign", methods=["POST"])
def stop_campaign():
    project_id = request.form["project_id"]
    package_id = request.form["package_id"]

    package = models.Package.query.get(package_id)
    npm.generate_package(project_id, package, False)
    package.campaign_active=False
    models.db.session.commit()
    return redirect("/project/{}".format(project_id))


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
        project_id=0
        protocol = callback.get("protocol", None)
        payload=None
        if protocol == "dns":
            subdomain = callback.get("data").get("subDomain", None)
            subdomain_split = subdomain.split('.')
            project_id = subdomain_split[0]
            payload = subdomain_split[1]
        elif protocol == "http":
            request=callback.get("data").get("request", None)
            request_decoded=base64_decode(request).decode('utf-8')
            json_string=regex.search(json_pattern, request_decoded)[0]
            json_parsed=json.loads(json_string)
            project_id=json_parsed.get("project_id", None)
            payload=json_parsed.get("payload", None)
        callback_record = models.Callback(protocol=callback.get("protocol", None), interactionString=callback.get("interactionString", None),
                                          time=callback.get("time"), client_ip=callback.get("client", None), request=callback.get("data").get("request", None),
                                          response=callback.get("data").get("response", None), subDomain=callback.get("data").get("subDomain", None),
                                          project_id=project_id, payload=payload)

        models.db.session.add(callback_record)
        models.db.session.commit()

    return "OK"
