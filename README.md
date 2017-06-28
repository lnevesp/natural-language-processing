# Natural Language Processing

### 1. Introduction

This project uses N-gram Language Model and Stupid Backoff algorithm to predict the next to word to be typed by a particular user. 
To speed up the process of creation of the N-Gram model a Map Reduce process was created. The goal is to compare the Language Model creation using both methods: Single and Multiprocess.

### 2. Data

The data comes from [The Open American National Corpus](http://http://www.anc.org/) and it is composed of two different corpora:  
  * **[OANC](http://www.anc.org/data/oanc/)** : 15 million words of contemporary American English with automatically-produced annotations for a variety of linguistic phenomena.  
  * **[MASC](http://www.anc.org/data/masc/)** : 500,000 words of OANC data equally distributed over 19 genres of American English, with manully produced or validated annotations for several layers of linguistic phenomena.  
  
The final corpus used in this project have XXXX words, XXXXX sentences and XXXX Mb.  
Based on the final accuracy and speed of Stupid-Backoff, a sample using 10% of the final corpus was selected to the final application. 
