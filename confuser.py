#!/usr/bin/env python3

import sys
import json

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def extract_packages_npm(filename):
    filename = sys.argv[1]
    file = open(filename)
    parsed = json.load(file)
    dependencies = parsed['dependencies']

    return dependencies

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        eprint("Specify requirements file to analyse")
        exit(1)

    dependencies = extract_packages_npm(sys.argv[1])
    
    for package, version in dependencies.items():
        print(package, version)
