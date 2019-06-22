import json
import argparse

parser = argparse.ArgumentParser(
    description='Adds metadata to a json file')
parser.add_argument('file')
args = parser.parse_args()

file = args.file
data = json.load(open(file, 'r'))

pytorch_ids = open("data/pytorch.ids", "r").readlines()
pytorch_ids = set([i.strip() for i in pytorch_ids])
tf_ids = open("data/tensorflow.ids", "r").readlines()
tf_ids = set([i.strip() for i in tf_ids])

for paper in data:
    paper['metadata']['words'] = set(paper['metadata']['words'])
    if paper['id'] in pytorch_ids:
        paper['metadata']['words'].add("pytorch")
    if paper['id'] in tf_ids:
        paper['metadata']['words'].add("tensorflow")
    paper['metadata']['words'] = list(paper['metadata']['words'])

with open(file, 'w') as f:
    json.dump(data, f, indent=2, sort_keys=True)
