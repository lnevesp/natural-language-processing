#!/usr/bin/env python

from collections import Counter
import fileinput

def createNgram( words, ngram):
    return zip(*[words[i:] for i in range(ngram)])

# TODO: Add pre counter - Add option for other methods to create NGrams
for line in fileinput.input():
    words = line.strip().split(',')
    for n in range(1, 6):
        ngrams_counts = Counter(createNgram(words, n))
        for ngram, count in ngrams_counts.items():
            print('{}\t{}'.format(','.join(ngram), count))