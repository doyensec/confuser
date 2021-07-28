import json
import sys

def extract_packages(filename):
    filename = sys.argv[1]
    file = open(filename)
    parsed = json.load(file)
    dependencies = parsed['dependencies']

    return dependencies