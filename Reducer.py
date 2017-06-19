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


# echo "hellow how are you" | /home/lneves/Dropbox/Data\ Science/Local\ MapReduce/local-mapreduce/lmr 5m 8 '/home/lneves/Softwares/Anaconda/Python3/bin/python3.6 Mapper.py' '/home/lneves/Softwares/Anaconda/Python3/bin/python3.6 Reducer.py' ./out4
