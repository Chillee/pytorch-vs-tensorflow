import uuid
import json
import os
import argparse
import requests

parser = argparse.ArgumentParser(
    description='Downloads research pdfs from a .json file')
parser.add_argument('file')
args = parser.parse_args()
file = args.file
data = json.load(open(file, 'r'))

print(f"Downloading papers for {file}")
for idx, paper in enumerate(data):
    print(f"Downloading \"{paper['name']}\" [{idx}/{len(data)}]")
    r = requests.get(paper['pdf_link'])
    with open(f"data/pdfs/{paper['id']}.pdf", 'wb') as f:
        f.write(r.content)
