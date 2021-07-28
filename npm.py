import json
import requests
import sys

NPM_ADDRESS = 'https://www.npmjs.com/'
PROXIES = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080',
}

def extract_packages(filename):
    filename = sys.argv[1]
    file = open(filename)
    parsed = json.load(file)
    dependencies = parsed['dependencies']

    return dependencies

def check_package_exists(package_name):
    # , proxies=PROXIES, verify=False)
    response = requests.get(NPM_ADDRESS + "package/" +
                            package_name, allow_redirects=False)

    return (response.status_code == 200)

def is_scoped(package_name):
    split_package_name = package_name.split('/')
    return (len(split_package_name) > 1)


def check_scope_exists(package_name):
    split_package_name = package_name.split('/')
    scope_name = split_package_name[0][1:]
    # ,  proxies=PROXIES, verify=False)
    response = requests.get(
        NPM_ADDRESS + "~" + scope_name, allow_redirects=False)

    return (response.status_code == 200)

def is_vulnerable(package_name):
    if (not check_package_exists(package_name)):
        if(is_scoped(package_name)):
            if (not check_scope_exists(package_name)):
                return True
        else:
            return True
    
    return False
