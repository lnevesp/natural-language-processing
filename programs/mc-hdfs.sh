#!/bin/bash

function usage() { echo "Usage: $0 [-k] <NUM_JOBS> <NUM_HASHING_SEGS> <MAPPER> <REDUCER> <OUTPUT_DIR>" 1>&2; exit 1; }

keep_mapper_out=false
while getopts "k" o; do
    case "${o}" in
        k)
            keep_mapper_out=true
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

if [ "$#" -ne 5 ]; then
    usage
fi
   
NUM_JOBS="$1"
NUM_HASHING_SEGS="$2"
MAPPER="$3"
REDUCER="$4"
OUTPUT_DIR="$5"

function timer()
{
    if [[ $# -eq 0 ]]; then
        echo $(date '+%s')
    else
        local  stime=$1
        etime=$(date '+%s')

        if [[ -z "$stime" ]]; then stime=$etime; fi

        dt=$((etime - stime))
        ds=$((dt % 60))
        dm=$(((dt / 60) % 60))
        dh=$((dt / 3600))
        printf '%d:%02d:%02d' $dh $dm $ds
    fi
}

START_TIME=$(timer)

HASHING_SCRIPT=`mktemp hashing.py.XXXX`
#echo hashing script $HASHING_SCRIPT
TEMPDIR=`mktemp -d mapper_tmp.XXXX`
{
    echo $' \e[1;32m>>>\e[m' Temporary output directory for mapper created: $'\e[1;32m'$TEMPDIR$'\e[m'
}>&2

function clean_up() {
   # echo $' \e[1;32m>>>\e[m' Cleaning...
    sleep 1
    if [ $keep_mapper_out = false ] ; then
        rm -r "$TEMPDIR"
        #&&
        #echo  $' \e[1;32m>>>\e[m' Temporary directory deleted: $'\e[1;32m'"$TEMPDIR"$'\e[m' ||
        #echo  $' \e[1;31m*\e[m' Failed to delete temporary directoy: $'\e[1;32m'"$TEMPDIR"$'\e[m'
    fi
    rm "$HASHING_SCRIPT"
} >&2
trap 'clean_up; exit' SIGHUP SIGINT SIGTERM 

cat <<EOF > "${HASHING_SCRIPT}"
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
import sys, re, os, fileinput, io
N_REDUCER, MAPPER_ID, BASE_DIR  = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]

def outfile(seg_id):
    segdir = '{}/reducer-{:02}'.format(BASE_DIR, seg_id)
    try: os.makedirs(segdir)
    except OSError : pass
    return io.open('{}/mapper-{:02}'.format( segdir, MAPPER_ID ), 'wt', encoding = 'utf-8')

seg_file = [ outfile(seg_id) for seg_id in range(N_REDUCER) ]

for line in fileinput.input(sys.argv[4:]):
    key, _,value = line[:-1].partition('\t')
    print( '{}\t{}'.format(key, value), file = seg_file[hash(key) % N_REDUCER])
fileinput.close()
for seg_id in range(N_REDUCER): seg_file[seg_id].close()
EOF


mkdir "$5" || exit 1
echo  $' \e[1;32m>>>\e[m' Mappers running...
parallel --no-notice --pipe -${NUM_JOBS}  --round-robin  --ungroup   "echo -n $'\e[s\e[F\e[2K           #{#}\e[u' ; ${MAPPER}  | python $HASHING_SCRIPT ${NUM_HASHING_SEGS} {#} $TEMPDIR " # pipe to here
echo
echo  $' \e[1;32m>>>\e[m' Mapper Elasped time: $'\e[1;32m'$(timer $START_TIME)$'\e[m'
echo  $' \e[1;32m>>>\e[m' Reducer running. Temporary input directory: $'\e[1;32m'"$TEMPDIR"$'\e[m'
REDUCER_TIME=$(timer)
parallel --no-notice --ungroup "sort -k 1,1 -t $'\t' -s {}/*  | ${REDUCER} > '${OUTPUT_DIR}/{/.}'"  ::: "${TEMPDIR}"/*
echo  $' \e[1;32m>>>\e[m' Reducer Elasped time: $'\e[1;32m'$(timer $REDUCER_TIME)$'\e[m'

{
    clean_up
    echo 
    if [ $keep_mapper_out = true ] ; then
        echo  $' \e[1;32m*\e[m' Mapper output directory: $'\e[1;32m'"$TEMPDIR"$'\e[m'
    fi
    echo  $' \e[1;32m>>>\e[m' $' \e[1;33m*\e[m' Elasped time: $'\e[1;32m'$(timer $START_TIME)$'\e[m'
    
} >&2
