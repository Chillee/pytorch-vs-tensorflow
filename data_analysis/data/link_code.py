import json
import glob
import os
import subprocess
from urllib.parse import urlparse

dirs = glob.glob('icml_code/*')
pt = open('icml_code/res_torch').readlines()
tf = open('icml_code/res_tensorflow').readlines()
pt = set([i.strip() for i in pt])
tf = set([i.strip() for i in tf])
url_data = {}
# print(dirs)
data = json.load(open('icml_2019.json'))
for i in dirs:
    process = subprocess.Popen(f'cd {i} && git config --get remote.origin.url', stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    url = output.decode('utf-8').strip()
    t = urlparse(url)
    frag = t.path.split('/')[-1]
    if frag.endswith('.git'):
        frag = frag[:-5]
    url_data[url] = set()
    if frag in tf:
        url_data[url].add('tf')
    if frag in pt:
        url_data[url].add('pt')

for paper in data:
    if 'code' not in paper['metadata']:
        continue
    if paper['metadata']['code'] in url_data:
        cur_data = url_data[paper['metadata']['code']]
        if 'tf' in cur_data:
            paper['metadata']['words'].append('tf')
        if 'pt' in cur_data:
            paper['metadata']['words'].append('pt')
json.dump(data, open('icml_2019_1.json', 'w'), sort_keys=True, indent=2)
# print(len(data))

