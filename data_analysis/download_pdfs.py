import uuid
import json
import os
import argparse
import requests
from urllib.parse import unquote

parser = argparse.ArgumentParser(
    description='Downloads research pdfs from a .json file')
parser.add_argument('file')
parser.add_argument('--redownload', default=False)
args = parser.parse_args()
file = args.file
redownload = args.redownload
data = json.load(open(file, 'r'))

print(f"Downloading papers for {file}")
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
}

for idx, paper in enumerate(data):
    if os.path.isfile(f"data/pdfs/{paper['id']}.pdf") and not redownload:
        print(f"Skipping \"{paper['name']}\"")
        continue
    else:
        print(f"Downloading \"{paper['name']}\" [{idx}/{len(data)}]")

    r = requests.get(unquote(paper['pdf_link']), headers=headers)
    with open(f"data/pdfs/{paper['id']}.pdf", 'wb') as f:
        f.write(r.content)
