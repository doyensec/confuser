# Confuser

## Installation

```
pip3 install -r requirements.txt
```

## Startup
```
python3 -m flask run --host=0.0.0.0 --port=1234
```

## Overview

An all-around tool to detect potential targets for dependency-confusion attacks. The flow starts with uploading a `package.json` file on the main page. After the backend analyses the packages looking for potentially injectable ones, it'll create a project in the tool. From the project view one can see injectable packages. Clicking "start campaign" will generate a payload and upload it to the NPM. Analogically, it's possible to stop the campaigns afterwards. Below the list of packages, there's also a list of callbacks given project has received.
