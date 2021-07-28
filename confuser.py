#!/usr/bin/env python3

import sys
import npm

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        eprint("Specify requirements file to analyse")
        exit(1)

    dependencies = npm.extract_packages(sys.argv[1])
    
    for package, version in dependencies.items():
        if (npm.is_vulnerable(package)):
            print(package, version)
