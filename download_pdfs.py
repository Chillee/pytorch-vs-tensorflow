import json
import os
import argparse

parser = argparse.ArgumentParser(
    description='Downloads research pdfs from a .json file')
parser.add_argument('file')
args = parser.parse_args()
file = args.file
data = json.load(open(data, 'r'))
print(len(data))
