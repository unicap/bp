#!/usr/bin/env python3

import os
from datetime import datetime
import calendar

from lxml import html
import requests
import json
import re
from threading import Thread

import yaml

from hashlib import md5

from geopy import Nominatim

import sys

geoloc = Nominatim()

if len(sys.argv) == 1:
    raise RuntimeError("Missing URL")
    URL = "https://sunnataofficial.bandcamp.com/album/zorya"
else:
    URL = sys.argv[1]


out = {}

filename = ".page_" + md5(URL.encode("UTF8")).hexdigest() + ".html"

if not os.path.exists(filename):
    page = requests.get(URL)
    with open(filename, "w") as f:
        f.write(page.content.decode("UTF-8"))


tree = None
with open(filename) as f:
    tree = html.fromstring(f.read())



def get_artist(tree):
    byartist = tree.xpath('//span[@itemprop="byArtist"]/*')[0]
    return byartist.text.strip(), byartist.attrib["href"]

def get_title(tree):
    title = tree.xpath('//h2[@itemprop="name"]')[0]
    return title.text.strip()

def parse_date(rawdate):
    months = {v: k for k,v in enumerate(calendar.month_name)}
    month_name, day, year = rawdate.split(" ")
    day = int(day.replace(",",""))
    month = months[month_name]
    year = int(year)
    return "%02d.%02d.%04d" % (day, month, year)

def get_release_date(tree):
    rawdate = tree.xpath("//div[contains(@class, 'tralbum-credits')]")[0].text.strip()
    tmp, rawdate = rawdate.split(" ", 1)
    date = parse_date(rawdate)
    return date

def get_tags(tree):
    tags = tree.xpath("//a[@class='tag']")
    tags = "BC: " + ", ".join([x.text for x in tags])
    return tags

artist_name, artist_url = get_artist(tree)
title = get_title(tree)
release_date = get_release_date(tree)
tags = get_tags(tree)

def escape(x):
    if ":" in x:
        x = '"' + x + '"'
    return x

print('- Album: %s' % (escape(title)))
print('  Artist: %s' % (escape(artist_name)))
print('  Genre: %s' % (escape(tags)))
print('  Links: %s' % (URL))
print('  Notes:')
print('  Rating:')
print('  Release: %s' % (release_date))
print('  Reviews:')

