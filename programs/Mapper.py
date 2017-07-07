#!/usr/bin/env python

from collections import Counter
import pickle

def createNgram( words, ngram):
    return zip(*[words[i:] for i in range(ngram)])

with open('../data/SampleTokens.pkl', "rb") as file:  # Unpickling
    TokensData = pickle.load(file)

for line in TokensData:
    for n in range(1, 6):
        ngrams_counts = Counter(createNgram(line, n))
        for ngram, count in ngrams_counts.items():
            print('{}\t{}'.format(','.join(ngram), count))