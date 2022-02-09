import json
from time import sleep
import requests
import os
import tempfile
import shutil
from flask import render_template

NPM_ADDRESS = 'https://www.npmjs.com/'
PROXIES = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def parse_package(file):
    return json.load(file)

def extract_packages(file):
    parsed = json.load(file)
    dependencies = parsed['dependencies']

    return dependencies

def check_package_exists(package_name):
    # , proxies=PROXIES, verify=False)
    response = requests.get(NPM_ADDRESS + "package/" +
                            package_name, allow_redirects=False, proxies=PROXIES, verify=False)

    return (response.status_code == 200)

def is_scoped(package_name):
    split_package_name = package_name.split('/')
    return (len(split_package_name) > 1)


def check_scope_exists(package_name):
    split_package_name = package_name.split('/')
    scope_name = split_package_name[0][1:]
    # ,  proxies=PROXIES, verify=False)
    response = requests.get(
        NPM_ADDRESS + "~" + scope_name, allow_redirects=False, proxies=PROXIES, verify=False)

    return (response.status_code == 200)

def is_vulnerable(package_name):
    if (not check_package_exists(package_name)):
        if(is_scoped(package_name)):
            if (not check_scope_exists(package_name)):
                return True
        else:
            return True
    
    return False

def get_vulnerable_packages(packages):
    #return [package for package in packages if is_vulnerable(package)]
    for package in packages:
        sleep(1) # prevent npm rate limit ban
        if is_vulnerable(package):
            yield package
        

def upload_package_by_npm(path):
    oldcwd = os.getcwd()
    os.chdir(path)
    os.system('npm pack --pack-destination=' + oldcwd)
    os.chdir(oldcwd)

def remove_package_by_npm(path):
    oldcwd = os.getcwd()
    os.chdir(path)
    #os.system('npm unpublish')
    os.chdir(oldcwd)

def generate_package(project_id, package, publish):
    with tempfile.TemporaryDirectory() as poc_dir:
        shutil.copy('payload_package/index.js', poc_dir)
        shutil.copy('payload_package/extract.js', poc_dir)
        packagejson_string = render_template("package.json", package_name=package.name, package_version=prepare_version_number(package.version), project_id=project_id)
        with  open(poc_dir + "/package.json", "w") as packagejson_file:
            packagejson_file.write(packagejson_string)
        if publish:
            upload_package_by_npm(poc_dir)
        else:
            remove_package_by_npm(poc_dir)

def prepare_version_number(version: str):
    if version[0].isnumeric():
        return version
    elif version[0] == '^':
        split_semver = version[1:].split('.')
        return "{}.{}.{}".format(split_semver[0], int(split_semver[1])+1, split_semver[2])
    elif version[0] == '~':
        split_semver = version[1:].split('.')
        return "{}.{}.{}".format(split_semver[0], split_semver[1], int(split_semver[2])+1)
    else:
        raise "Broken version number"