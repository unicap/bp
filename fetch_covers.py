#!/usr/bin/env python3

from datetime import datetime
import subprocess
import os
import sys
import shlex
import yaml

filename = sys.argv[1]

filename = sys.argv[1]

with open(filename) as f:
    albums = yaml.load(f)

albums = sorted(albums, key=lambda x: x["Release"])

# Get month, year and create directory name
datestr = albums[0]["Release"]
date = datetime.strptime(datestr, "%d.%m.%Y")
month = date.strftime("%B")
dirname = month + "_" + str(date.year)

if not os.path.exists(dirname):
    os.mkdir(dirname)

for a in albums:
    artist = a["Artist"]
    album = a["Album"]
    destpath = os.path.join(dirname, shlex.quote(album)+".jpg")

    if os.path.exists(destpath):
        continue

    print("Processing "+ album)
    try:
        subprocess.run(["sacad", artist, album, "600", destpath])
    except TypeError as e:
        print("Error:",e)
        print("artist:", artist)
        print("album:", album)
