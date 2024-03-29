import datetime
import json
from time import time
import regex
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_wtf.csrf import CSRFProtect
from itsdangerous import base64_decode
from sqlalchemy import func
import npm
import os


from burp import BurpCollaboratorClient
import models

json_pattern = r'\{(?:[^{}]|(?R))*\}'

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///confuser.db'
csrf = CSRFProtect(app)
models.db.init_app(app)
with app.app_context():
    models.db.create_all()

@app.template_filter('datetime')
def format_date(epoch):
    return datetime.datetime.fromtimestamp(epoch/1000.0).strftime("%m/%d/%Y, %H:%M:%S")

@app.route("/")
def main():
    all_packages_subquery = models.db.session.query(models.Package.project_id, func.count(models.Package.id).filter(models.Package.vulnerable == True).label("count")).group_by(models.Package.project_id).subquery()
    projects = models.db.session.query(models.Project, all_packages_subquery.c.count).join(all_packages_subquery, all_packages_subquery.c.project_id == models.Project.id, isouter=True).order_by(all_packages_subquery.c.count.desc()).all()

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
    dependencies = (package.get("dependencies") if package.get("dependencies") else {}) | (package.get("devDependencies") if package.get("devDependencies") else {}) | (package.get("optionalDependencies") if package.get("optionalDependencies") else {})
    uncached_dependencies = []
    for dependency in dependencies.keys():
        cached_entry = models.PackageCache.query.filter_by(name=dependency).first()
        if not cached_entry:
            uncached_dependencies.append(dependency)

    vulnerable_dependencies = npm.get_vulnerable_packages(uncached_dependencies)
    vulnerable_dependencies = list(vulnerable_dependencies)

    for dependency in dependencies.keys():
        package_record = models.Package(dependency, dependencies.get(
            dependency), dependency in vulnerable_dependencies)
        project_record.packages.append(package_record)

    for dependency in uncached_dependencies:
        if dependency not in vulnerable_dependencies:
            cache_record = models.PackageCache(dependency, time())
            models.db.session.add(cache_record)

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

@app.route("/project/false_positive", methods=["POST"])
def false_positive():
    project_id = request.form["project_id"]
    package_id = request.form["package_id"]
    package = models.Package.query.get(package_id)
    package.vulnerable = False

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
        elif protocol == "http" or protocol == "https":
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
