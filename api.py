from flask import Flask
from flask import render_template
from flask import request
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
        
@app.route("/generate_poc")
def generate_poc():
    package_name = request.args.get('package')
    if not package_name:
        return "Provide package name.", 400

    npm.create_poc(package_name)
    return package_name