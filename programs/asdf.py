
from __future__ import print_function, unicode_literals
import sys, re, os, fileinput, io
N_REDUCER, MAPPER_ID, BASE_DIR  = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]

def outfile(seg_id):
    segdir = '{}/reducer-{:02}'.format(BASE_DIR, seg_id)
    try: os.makedirs(segdir)
    except OSError:
        pass
    return io.open('{}/mapper-{:02}'.format( segdir, MAPPER_ID ), 'wt', encoding = 'utf-8')

seg_file = [ outfile(seg_id) for seg_id in range(N_REDUCER) ]

for line in fileinput.input(sys.argv[4:]):
    key, _,value = line[:-1].partition('\t')
    print( '{}\t{}'.format(key, value), file = seg_file[hash(key) % N_REDUCER])
fileinput.close()
for seg_id in range(N_REDUCER): seg_file[seg_id].close()