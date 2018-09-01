#!/usr/bin/env python3

import sys

import yaml

from yattag import Doc, indent

doc, tag, text = Doc().tagtext()

filename = sys.argv[1]

albums = None

with open(filename) as f:
    albums = yaml.load(f)

albums = sorted(albums, key=lambda x: x["Release"])

intro = """
<a href="https://www.betreutesproggen.de/wp-content/uploads/2018/09/collage.jpg"><img src="https://www.betreutesproggen.de/wp-content/uploads/2018/09/collage.jpg" alt="" width="800" height="600" class="alignleft size-full wp-image-46497" /></a>&nbsp;
<p><b>In der <a href="https://www.betreutesproggen.de/tag/releasecorner" rel="nofollow" target="_blank">#ReleaseCorner</a> sammeln wir monatsweise bemerkenswerte Neuerscheinungen aus dem progrelevanten Umfeld (vgl. auch unsere weiteren Service-Ecken <a href="https://www.betreutesproggen.de/tag/vinylcorner/" rel="nofollow" target="_blank">VinylCorner</a> sowie <a href="https://www.betreutesproggen.de/tag/crowdfundingcorner" rel="nofollow" target="_blank">CrowdfundingCorner/</a>). Fehlt ein wichtiges Album? Wir freuen uns über Hinweise in der <a href="https://www.facebook.com/groups/219926581943031/">Betreuter-Gruppen-Prog Gruppe</a> auf Facebook oder über das Kontaktformular am Ende dieses Beitrags.</b></p>
"""

doc.asis(intro)
linenr = 0
for album in albums:
    colorstr = ""
    if linenr % 2:
        colorstr = "background-color:#e7e7e7;"
    linenr += 1

    with tag("div", style=colorstr):
        with tag("div"):
            with tag("div", style='width:45%; display: inline-block; vertical-align:top;'):
                with tag("p"):
                    with tag("b"):
                        text(album["Artist"])
                    doc.stag("br")
                    with tag("em"):
                        text(album["Album"])
                    doc.stag("br")
                    text(" VÖ: ", album["Release"])
                    doc.stag("br")
                    text("Genre: ", album["Genre"])
            with tag("div", style='width:50%; display: inline-block; vertical-align:top;'):
                links = album["Links"]
                review = album["Reviews"]
                if type(links) == str:
                    links = [links]
                if links or review:
                    with tag("p"):
                        if links:
                            with tag("b"):
                                text("Links:")
                            #doc.stag("br")
                            for link in links:
                                linktxt = link[:40]
                                if len(linktxt) < len(link):
                                    linktxt += "..."
                                with tag("a", href=link):
                                    text(linktxt)
                            #doc.stag("br")
                        if review:
                            with tag("b"):
                                text("Review auf BetreutesProggen.de / den BBS:")
                            #doc.stag("br")
                            reviewtxt = review[:40]
                            if len(reviewtxt) < len(review):
                                reviewtxt += "..."
                            with tag("a", href=review.split()[-1]):
                                text(reviewtxt)
        with tag("div", style="margin-top:-2em;"):
            if album["Notes"]:
                with tag("p"):
                    text(album["Notes"])
            else:
                text(" ")

footer = """


Es fehlt etwas? Hinweise bitte über das Kontaktformular:

[contact-form-7 id="108" title="Ohne Titel"]
"""
doc.asis(footer)


print (indent(doc.getvalue()))
