import json
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(
    description='Adds metadata to a json file')
parser.add_argument('file')
args = parser.parse_args()

file = args.file
data = json.load(open(file, 'r'))

words = ["pytorch", "tensorflow", "google.com", "fb.com"]
mapping = {
    'fb.com': "facebook",
    "google.com": "google"

}
word_sets = defaultdict(set)
for paper in data:
    for word in words:
        if word in paper['metadata']['words']:
            word_sets[word].add(paper['id'])

print(len(word_sets['']))
