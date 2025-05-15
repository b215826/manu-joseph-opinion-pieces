#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from readability import Document
from subprocess import run
from pathlib import Path
import re

def extract_links(name="links.html"):
    with open(name) as html:
        soup = BeautifulSoup(html, features="lxml")

    links = []
    for h2 in soup.find_all("h2", class_="headline"):
        links.append(h2.find("a").get("href"))

    with open("links.txt", "w") as fd:
        fd.write("\n".join(links))

def download_links(name="links.txt"):
    Path("./html").mkdir(exist_ok=True)
    run(f"wget --continue --directory-prefix ./html --input-file={name}".split())

def html2md(name):
    with open(name) as fd:
        html = fd.read()

    if m := re.search(r'"datePublished":[^"]*"([^"]*)"', html):
        date = m.group(1)
        date = date.split("T")[0]

    doc = Document(html)
    content = doc.summary()
    content = re.sub(r"<a\b[^>]*>(.*?)<\/a>", r"\1", content, flags=re.IGNORECASE)

    title = doc.short_title()
    title = title.strip()
    title = re.sub(r"^Manu Joseph\W*", "", title)
    title = re.sub(r"^Opinion\W*", "", title)

    output = title.lower()
    output = re.sub(r"[^a-z0-9.-]+", "_", output)
    output = re.sub(r"(_+$|^_+)", "", output)
    output = f"md/{date}-{output}.md"

    md = run("pandoc -f html -t markdown_strict".split(),
             input=content,
             text=True,
             capture_output=True)

    Path("./md").mkdir(exist_ok=True)
    with open(output, "w") as fd:
        fd.write(f"# {title}\n\n")
        fd.write(f"*{date}*\n\n")
        fd.write(md.stdout)

def process_html():
    for path in Path("html/").rglob("*.html"):
        try:
            html2md(path)
            print(f"processed {path}")
        except:
            print(f"ERROR: failed for {path}")

if __name__ == "__main__":
    extract_links()
    download_links()
    process_html()
