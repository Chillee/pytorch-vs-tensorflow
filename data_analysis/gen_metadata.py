import json
import argparse
import glob

files = glob.glob("data/*.json")
for file in files:
    data = json.load(open(file, 'r'))

    words = ["pytorch", "tensorflow", "google.com",
             "fb.com", "opennmt", "allennlp", "google brain"]
    for word in words:
        id_list = open(f"data/{word}.ids", "r").readlines()
        id_list = set([i.strip() for i in id_list])

        for paper in data:
            paper['metadata']['affiliation'] = []
            turn_into_sets = ['words', 'affiliation']
            for i in turn_into_sets:
                paper['metadata'][i] = set(paper['metadata'][i])
            if paper['id'] in id_list:
                paper['metadata']['words'].add(word)

            for i in turn_into_sets:
                paper['metadata'][i] = list(paper['metadata'][i])

    with open(file, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
