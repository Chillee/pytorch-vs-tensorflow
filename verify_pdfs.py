# Removes pdfs that aren't in a json file
import json
import glob
from os.path import basename
import os

files = glob.glob("data/*.json")
ids = []
for file in files:
    with open(file) as f:
        data = json.load(f)
        for paper in data:
            ids.append(paper['id'])
pdfs = glob.glob("data/pdfs/*.txt")
for pdf in pdfs:
    paper_id = basename(pdf).split('.')[0]
    if paper_id not in ids:
        print(f"Removing {paper_id}")
        os.remove(pdf)
