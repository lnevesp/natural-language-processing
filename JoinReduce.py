import glob
from collections import Counter, defaultdict
import pandas as pd


ReduceOutput = glob.glob('../data/MapReduce/*')

DataPath = '../data/'

with open(DataPath + "FullNgrams.txt", 'w') as outfile:
    for fname in ReduceOutput:
        with open(fname) as infile:
            for line in infile:
                outfile.write(line)

# Divide N-Gram by type
FullNgram = open(DataPath + "FullNgrams.txt")
FullNgram = FullNgram.readlines()

ngram_counts = defaultdict(Counter)  # Creates an empty dictionary

# Fill the ngram_counts dictionary with the
ngramDict = defaultdict(list)
for line in FullNgram:
    line = line.strip()
    ngram, count = line.split('\t', 1)
    length = len(ngram.split(','))
    if length == 1:
        ngram, count = ngram, int(count)
        ngram_counts[length][ngram] += count
    else:
        ngram, count = tuple(ngram.split(',')), int(count)
        ngram_counts[length][ngram] += count



"""Separate Ngrams into 5 Datasets"""
labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]  # Columns Names
Ngram = [1, 2, 3, 4, 5]  # Ngram types

for i in Ngram:
    ngramDict = defaultdict(list)
    ngramDict = dict(ngram_counts[i])
    # NgramFinal = pd.DataFrame(ngramDict, columns=labels[(5 - int(i)):])
    NgramFinal = pd.DataFrame.from_dict(ngramDict, orient='index').reset_index()
    NgramFinal = NgramFinal.rename(columns={'index': 'Ngram', 0: 'count'})

    filename = "../data/Ngram" + str(i) + ".csv"
    with open(DataPath + filename, 'w') as outfile:
        for line in NgramFinal:
            ngram = line[['Ngram']].split()
            ngram.append(line['count'])
            outfile.write(line)

