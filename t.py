
# %%
import json
import argparse
from collections import defaultdict
import glob
from os import path

# parser = argparse.ArgumentParser(
#     description='Adds metadata to a json file')
# parser.add_argument('file')
# args = parser.parse_args()

# file = args.file
files = glob.glob('data/*.json')
confs = defaultdict(dict)
for file in files:
    data = json.load(open(file, 'r'))
    conf_name = path.basename(file).split('.')[0]
    conf_name, year = conf_name.split('_')
    data = json.load(open(file, 'r'))
    for paper in data:
        try:
            paper['text'] = open(
                f"data/pdfs/{paper['id']}.txt", 'r').read().lower()
        except:
            paper['text'] = "N/A"
            pass
    confs[conf_name][year] = data


# %%
synonyms = {
    'facebook': ["facebook ai research", 'fb.com'],
    'google': ['google.com', 'google brain'],
    'pytorch': ['pytorch', 'allennlp', 'opennmt-py'],
    'tensorflow': ['tensorflow', 'opennmt-tf'],
    'stanford': ['@cs.stanford.edu', '@stanford.edu']
}
for k, v in synonyms.items():
    synonyms[k] = [i.lower() for i in v]

words = set([i for k, v in synonyms.items() for i in v])
mapping = defaultdict(list)
for k, vs in synonyms.items():
    for v in vs:
        mapping[v].append(k)
# print(mapping)

word_sets = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
for conf in confs:
    for year in confs[conf]:
        data = confs[conf][year]
        word_set = word_sets[conf][year]
        for paper in data:
            for word in words:
                if word in paper['text']:
                    if word in mapping:
                        for key in mapping[word]:
                            word_set[key].add(paper['id'])


# %%
conf = 'naacl'
for year in sorted(confs[conf]):
    ws = word_sets[conf][year]
    print(year)
    print("total papers", len(confs[conf][year]))
    print("pytorch", len(ws['pytorch']))
    print("pytorch independent", len(ws['pytorch'] - ws['facebook']))
    print("tensorflow", len(ws['tensorflow']))
    print("tensorflow independent", len(ws['tensorflow'] - ws['google']))
    print()


# %%
