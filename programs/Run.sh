#!/bin/bash

echo $' \e[1;33m>>>\e[m' Running Words Prediction

file="../data/FullNgrams.csv"
if [ ! -f "$file" ]
then
   python LanguageModel.py 
else
   echo $' \e[1;33m>>>\e[m' Language Model Already Created
fi

echo
python Train.py
