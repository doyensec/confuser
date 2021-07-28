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
    response = requests.get(NPM_ADDRESS + "package/" + package_name)#, proxies=PROXIES, verify=False)
    print(response.status_code)
    return (response.status_code == 200)
