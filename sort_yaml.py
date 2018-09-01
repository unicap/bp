#!/usr/bin/env python3

import sys

import yaml

filename = sys.argv[1]

albums = None


with open(filename) as f:
    s = f.read()

albums = yaml.load(s)
albums = sorted(albums, key=lambda x: x["Release"])

s = yaml.dump(albums, default_flow_style=False, explicit_start=True, allow_unicode=True)
s = s.replace("\n- ", "\n\n- ")
s = s.replace(": null", ":")
with open(filename, "w") as f:
    f.write(s)
