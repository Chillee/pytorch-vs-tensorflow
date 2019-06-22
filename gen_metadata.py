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
    paper['metadata']['affiliation'] = []
    turn_into_sets = ['words', 'affiliation']
    for i in turn_into_sets:
        paper['metadata'][i] = set(paper['metadata'][i])
    if paper['id'] in pytorch_ids:
        paper['metadata']['words'].add("pytorch")
    if paper['id'] in tf_ids:
        paper['metadata']['words'].add("tensorflow")
    for author in paper['authors']:
        google_names = ["google", "deepmind"]
        fb_names = ["facebook", "aml", "fair"]
        for name in google_names:
            if author[1].lower().find(name) != -1:
                paper['metadata']['affiliation'].add('google')
        for name in fb_names:
            if author[1].lower().find(name) != -1:
                paper['metadata']['affiliation'].add('facebook')

    for i in turn_into_sets:
        paper['metadata'][i] = list(paper['metadata'][i])

with open(file, 'w') as f:
    json.dump(data, f, indent=2, sort_keys=True)
