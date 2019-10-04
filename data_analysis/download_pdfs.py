import uuid
import json
import os
import argparse
import requests
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

parser = argparse.ArgumentParser(
    description='Downloads research pdfs from a .json file')
parser.add_argument('file')
parser.add_argument('--redownload', default=False)
args = parser.parse_args()
file = args.file
redownload = args.redownload
data = json.load(open(file, 'r'))


driver = webdriver.Chrome()
driver.implicitly_wait(10)
print(f"Downloading papers for {file}")
ignored = [503, 504, 505] + list(range(506, 515))
for idx, paper in enumerate(data):
    if os.path.isfile(f"data/pdfs/{paper['id']}.pdf") and not redownload:
        print(f"Skipping \"{paper['name']}\"")
        continue
    elif idx in ignored:
        print("ignored for w.e. reason")
        continue
    else:
        print(f"Downloading \"{paper['name']}\" [{idx}/{len(data)}]")
    link = unquote(paper['pdf_link'])
    link = link.replace('pdf', 'forum')
    driver.get(link)
    pdf_link = driver.find_element_by_css_selector('.note_content_value > a').get_attribute('href')
    pdf_link = pdf_link.replace('abs', 'pdf')
    pdf_link += '.pdf'
    print(pdf_link)

    r = requests.get(pdf_link)
    with open(f"data/pdfs/{paper['id']}.pdf", 'wb') as f:
        f.write(r.content)
