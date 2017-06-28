#!/usr/bin/env python
import fileinput
from collections import Counter, defaultdict

ngram_counts = defaultdict(Counter)
for line in fileinput.input():
    ngram, count = line.split('\t', 1)
    ngram, count = tuple(ngram.split(' ')), int(count)
    length = len(ngram)
    ngram_counts[length][ngram] += count

for length in ngram_counts:
    for ngram, count in ngram_counts[length].items():
        print ('{}\t{}'.format(' '.join(ngram), count))


# // echo "Word Prediction" | /home/lneves/Dropbox/Data\ Science/Local\ MapReduce/local-mapreduce/lmr 5m 8 'python Mapper.py' 'python Reducer.py' ../data/MapReduceOutput_00001
