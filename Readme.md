# Confuser

A tool to detect Dependency Confusion vulnerabilities. It allows scanning ```packages.json``` files, generating and publishing payloads to the NPM repository, and finally aggregating the callbacks from vulnerable targets.

## Installation
```
pip3 install -r requirements.txt
```

## Usage
```
python3 -m flask run --host=0.0.0.0 --port=1234
```
The flow starts with uploading a `package.json` file on the main page. The backend will analyze all packages looking for potentially vulnerable ones. From within the project page, it will be possible to review the list of packages. By clicking on "start campaign", the tool generates a new payload and uploads it to the NPM repository. By clicking on "stop campaign", it is possible to remove the package and clean up the environment.
