#!/usr/bin/env python
import re
import fileinput
from collections import Counter

def tokens(str1): return re.findall('[a-z]+', str1.lower())

def to_ngrams( words, length):
    return zip(*[words[i:] for i in range(length)])  

for line in fileinput.input():
    words = tokens(line)
    for n in range(1, 6):
        ngrams_counts = Counter(to_ngrams(words, n))
        for ngram, count in ngrams_counts.items():
            print ('{}\t{}'.format(' '.join(ngram), count))