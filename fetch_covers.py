#!/usr/bin/env python3

from datetime import datetime
import subprocess
import os
import sys
import shlex

filename = sys.argv[1]
tablestr = ""

with open(filename) as f:
    tablestr = f.read()

tablestr = tablestr.strip()

# split to lines, skip header
lines = tablestr.split("\n")[2:]

# Get month, year and create directory name
datestr, artist, album, genre, links, txt, review = [x.strip() for x in lines[0].split("|")][1:-1]
date = datetime.strptime(datestr, "%d.%m.%Y")
month = date.strftime("%B")
dirname = month + "_" + str(date.year)

if not os.path.exists(dirname):
    os.mkdir(dirname)

for line in lines:
    try:
        datestr, artist, album, genre, links, txt, review = [x.strip() for x in line.split("|")][1:-1]
    except ValueError:
        print("Error parsing: ", line)
        print(line.split("|"))

    print("Processing "+ album)
    subprocess.run(["sacad", artist, album, "600", os.path.join(dirname, shlex.quote(album)+".jpg")])
