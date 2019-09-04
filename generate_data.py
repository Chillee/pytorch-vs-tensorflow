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
    'facebook': ["facebook ai research", 'fb.com'],
    'google': ['google.com', 'google brain'],
    'pytorch': ['pytorch', 'allennlp', 'opennmt-py', 'torchvision', 'huggingface', 'fairseq'],
    # 'opennmt': ['opennmt-py', 'opennmt-tf'],
    'tensorflow': ['tensorflow', 'opennmt-tf'],
    # 'keras': ['keras'],
    # 'stanford': ['@cs.stanford.edu', '@stanford.edu'],
    # 'mit': ['@csail.mit.edu', '@mit.edu'],
    # 'uw': ['@cs.washington.edu', '@washington.edu'],
    # 'cornell': ['@cs.cornell.edu', '@cornell.edu'],
    # 'cmu': ['@cmu.edu', '@cs.cmu.edu'],
    # 'theano': ['theano'],
    # 'deepmind': ['deepmind'],
    # 'mxnet': ['mxnet'],
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

ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(years_fmt)
ax.xaxis.set_minor_locator(months)
ax.set_xlim(np.datetime64('2017'), np.datetime64('2020'))
ax.set_facecolor((1, 1, 1, 1))
plt.rcParams["figure.figsize"] = (15, 10)
plt.tick_params(labelright=True)
prop_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
nlp_confs = ['naacl', 'acl', 'emnlp']
cv_confs = ['cvpr', 'eccv', 'iccv']
ml_confs = ['nips', 'iclr', 'icml']
csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)
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
        biased_set = ws['facebook']csvfile.close()

legend1 = plt.legend(handles=[solid_line, dashed_line], loc=4)
plt.legend()
plt.grid()
plt.gca().add_artist(legend1)

plt.title("Original vs. Keras Corrected")
plt.show()
