#!/usr/local/bin/python3


import json
import argparse


def jsonformat(filename):
    with open(filename) as f:
        data = json.load(f)

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="filename for formatting")
    parser.add_argument("-q", "--quiet", help="increase output verbosity",
                        action="store_true")
    args = parser.parse_args()
    if not args.quiet:
        print("Parsing and outputting file:")
    jsonformat(args.filename)
    if not args.quiet:
        print("Done.")
