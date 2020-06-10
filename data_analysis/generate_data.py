import matplotlib.style as style
import json
import argparse
from collections import defaultdict
import glob
from os import path
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np
import csv

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

begin = time.time()
synonyms = {
    'facebook': ["facebook ai research", '@fb.com'],
    'google': ['@google.com', 'google brain'],
    'pytorch': ['pytorch', 'allennlp', 'opennmt-py', 'torchvision', 'fairseq'],
    # 'opennmt': ['opennmt-py', 'opennmt-tf'],
    'tensorflow': ['tensorflow', 'opennmt-tf', 'keras'],
    # 'keras': ['keras'],
    # 'stanford': ['@cs.stanford.edu', '@stanford.edu'],
    # 'mit': ['@csail.mit.edu', '@mit.edu'],
    # 'uw': ['@cs.washington.edu', '@washington.edu'],
    # 'cornell': ['@cs.cornell.edu', '@cornell.edu'],
    # 'cmu': ['@cmu.edu', '@cs.cmu.edu'],
    # 'theano': ['theano'],
    # 'deepmind': ['deepmind'],
    'mxnet': ['mxnet'],
    'jax': ['jax'],
    # 'dynet': ['dynet'],
    # 'autobatching': ['auto-batching', 'autobatching'],
    # 'parsing': ['parsing'],
    # 'paddle': ['paddlepaddle']
    #     'architecture search': ['architecture search'],
    #     'gan': ['generative adversarial network'],
    #     'rl': ['reinforcement learning'],
    #     'bayesian': ['bayesian'],
    #     'meta-learning': ['meta-learning', 'metalearning'],
    #     'few-shot': ['few shot', 'few-shot', 'one shot', 'one-shot'],
    #     'graph': ['graph neural network'],
    #     'generative': ['generative model'],
    #     'adversarial': ['adversarial attack', 'ifgsm'],
}
for k, v in synonyms.items():
    synonyms[k] = [i.lower() for i in v]

words = set([i for k, v in synonyms.items() for i in v])
mapping = defaultdict(list)
for k, vs in synonyms.items():
    for v in vs:
        mapping[v].append(k)
        mapping[v].append(v)

word_sets = defaultdict(lambda: defaultdict(lambda: defaultdict(set)))
for conf in confs:
    for year in confs[conf]:
        data = confs[conf][year]
        word_set = word_sets[conf][year]
        for paper in data:
            # if 'decision' in paper['metadata'] and 'Accept' not in paper['metadata']['decision']:
            #     continue
            for word in words:
                if word in paper['text']:
                    if word in mapping:
                        for key in mapping[word]:
                            word_set[key].add(paper['id'])

print(time.time() - begin)

conf_month = {
    'eccv': 'september',
    'acl': 'july',
    'naacl': 'june',
    'acl': 'august',
    'icml': 'june',
    'cvpr': 'june',
    'nips': 'december',
    'aistats': 'april',
    'colt': 'june',
    'iclr': 'may',
    'iccv': 'november',
    'emnlp': 'november'
}
conf_month = {
    k: time.strptime(v, '%B').tm_mon for k, v in conf_month.items()}
style.use('default')


years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
years_fmt = mdates.DateFormatter('%Y')

fig, ax = plt.subplots()

# ax.set_ylim(0,125)

nlp_confs = ['naacl', 'acl', 'emnlp']
cv_confs = ['cvpr', 'eccv', 'iccv']
ml_confs = ['nips', 'iclr', 'icml']
csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)
conf_map = {
    'nips': "NeurIPS"
}
for conf in confs:
    if conf == 'colt' or conf == 'aistats':
        continue
    pytorch = []
    pytorch_corr = []
    tf = []
    tf_corr = []
    dates = []
    print(conf)
    for year in sorted(confs[conf]):
        ws = word_sets[conf][year]
        date = np.datetime64(f"{year}-{conf_month[conf]:02}")
        dates.append(date)
        pytorch_set = ws['pytorch'] - ws['tensorflow']
        tf_set = ws['tensorflow'] - ws['pytorch']
        biased_set = ws['facebook'] | ws['google']

        pytorch.append(len(pytorch_set))
        tf.append(len(tf_set))
        pytorch_corr.append(len(pytorch_set - biased_set))
        tf_corr.append(len(tf_set - biased_set))
        conf_display = conf.upper()
        if conf in conf_map:
            conf_display = conf_map[conf]
        else:
            conf_display = conf.upper()

        writer.writerow([conf_display, f"{conf_month[conf]:02}/{year[2:]}",
                         pytorch_corr[-1], tf_corr[-1], len(confs[conf][year])])
csvfile.close()
