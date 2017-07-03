#!/usr/bin/env python

from collections import Counter
import pickle
import datetime

# time = datetime.datetime.now().time().strftime('%H:%M:%S')
# print("Starting Mapper" + time)

def createNgram( words, length):
    return zip(*[words[i:] for i in range(length)])

with open('../data/SampleTokens.pickle', "rb") as file:  # Unpickling
    TokensData = pickle.load(file)

# print("Starting MAPREDUCE! " + time)
for line in TokensData:
    for n in range(1, 6):
        ngrams_counts = Counter(createNgram(line, n))
        for ngram, count in ngrams_counts.items():
            print('{}\t{}'.format(','.join(ngram), count))