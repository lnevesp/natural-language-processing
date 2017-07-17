#!/bin/bash

echo $' \e[1;33m>>>\e[m' Running Words Prediction



File01="../data/ANC_Corpora.tar.gz"
File02="../data/Tokens.txt"
File03="../data/FullNgrams.csv"


if [ ! -f "$FileOrininal" ]
    echo lindo
 then
   python LanguageModel.py 
elif
    [ ! -f "$fil" ]
   echo $' \e[1;33m>>>\e[m' Language Model Already Created
fi

echo
python Train.py
