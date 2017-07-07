#!/usr/bin/env python
import fileinput
from collections import Counter, defaultdict

ngram_counts = defaultdict(Counter)

for line in fileinput.input():
    line = line.strip()
    ngram, count = line.split('\t', 1)
    length = len(ngram.split(','))
    ngram, count = tuple(ngram.split(',')), int(count)
    ngram_counts[length][ngram] += count

for length in ngram_counts:
    print(length)
    for ngram, count in ngram_counts[length].items():
        print('{},{}'.format(','.join(ngram), count))


# // echo "Word Prediction" | /home/lneves/Dropbox/Data\ Science/Local\ MapReduce/local-mapreduce/lmr 5m 8 'python Mapper.py' 'python Reducer.py' ../data/MapReduceOutput_00001
