from nltk.tokenize import word_tokenize
import re
import html
import sys
import os.path
import Formats as of
import pandas as pd
import numpy as np


class CleanCorpus:

    def __init__(self, Corpus = "../data/Corpus.txt", infoLog = pd.DataFrame(np.array([["0001"]]), columns=['ProcessID'])):
        self.color01 = "\033[92m"  # Green
        self.infoLog = infoLog  # Log Dataframe

        # Print Start Time
        StartScript = of.calcTime()
        of.StartScript(time=StartScript, phrase="Running CleanData.py")

        if os.path.isfile("../data/Corpus.txt") != 1:
            of.NormalMessage(phrase="Corpus.txt not created. Please, run DownloadFiles.py")
            self.infoLog['Count_CorpusLines'] = None
            self.infoLog["Count_WordTokens"] = None
            self.infoLog['Time_cleanCorpus'] = None
            self.infoLog['Time_ReadCorpus'] = None
        else:
            # Read Corpus =============================================================================================+
            StartTime = of.calcTime()
            of.ElapseStart(time=StartTime, phrase="Reading Corpus")

            Corpus = open(Corpus)
            Corpus = Corpus.readlines()
            self.infoLog['Count_CorpusLines'] = int(len(Corpus))

            # Print time elapse
            self.infoLog['Time_ReadCorpus'] = float(of.deltaTime(start=StartTime))
            of.ElapseEnd(start=StartTime)

            if os.path.isfile("../data/Tokens.txt") != 1:  # Check if the file already exists

                # Create Corpus =======================================================================================+
                StartTime = of.calcTime()
                self.cleanCorpus(Corpus)  # Read Raw Corpus
                self.infoLog['TokensSize'] = round(os.path.getsize("../data/Tokens.txt") / (1024 * 1024.0), 2)
                self.infoLog['Time_cleanCorpus'] = float(of.deltaTime(start=StartTime))  # Calculate Time Elapse
                of.ElapseEnd(start=StartTime)  # Print time Elapse

            else:
                of.NormalMessage(phrase="Tokens already created")
                self.infoLog['FileSize_Tokens'] = round(os.path.getsize("../data/Tokens.txt") / (1024 * 1024.0), 2)
                self.infoLog["Count_WordTokens"] = None
                self.infoLog['Time_cleanCorpus'] = None
                self.infoLog['Time_ReadCorpus'] = None

            # Print Final Time
        self.infoLog['Time_CleanScript']=float(of.deltaTime(start=StartScript))
        of.EndScript(start=StartScript, phrase="CleanData.py Finished")
        # print(self.infoLog)

    # Function: Remove Punctuation ------------------------------------------------------------------------------------+
    def removePunctuation(self, tokens):
        regex = re.compile('[^a-zA-Z]')

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)
        return words_vector_RP

    # Function: Create Tokens for each line ---------------------------------------------------------------------------+
    def createTokens(self, line):
        words_vector = []  # Creates an empty list
        line = html.unescape(line)  # Removes HTML or XML character references and entities.
        line = [x for x in map(str.strip, line.split('.')) if x]  # Splits  Lines on Period
        line = [x.lower() for x in line]  # Convert to lowercase
        for Sentence in line:
            Sentence = Sentence.strip()  # Deletes the /n on each sentence
            Sentence = ''.join(i for i in Sentence if not i.isdigit())  # Remove numbers
            words = word_tokenize(Sentence)  # Convert lines into word vector (tokenizing)
            words = self.removePunctuation(tokens=words)  # Removes punctuation
            words_vector.append(words)  # Appends the tokens
        return words_vector

    # Function: Clean Data --------------------------------------------------------------------------------------------+
    """Read the Raw Corpus, returns all sentences tokenized and cleaned"""
    def cleanCorpus(self, Corpus):
        StartTime = of.calcTime()
        self.Tokens = []
        self.infoLog["Count_WordTokens"] = 0
        i = 0
        TotalLines = len(Corpus)
        with open("../data/Tokens.txt", 'w') as outfile:
            for line in Corpus:
                i += 1
                sys.stdout.write("\r" + self.color01 + ">>>  " + StartTime + "\033[0m" +
                                 " Cleaning Data" + self.color01 + " | " + "\033[0m" + "Line: " +
                                 self.color01 + str(i) + "/" + str(TotalLines) +
                                 " (" + str(round((i/TotalLines)*100, 2)) + "%)" + "\033[0m")
                sys.stdout.flush()
                LineToken = self.createTokens(line=line)
                if LineToken:
                    for line in LineToken:
                        wordcount = len(line)
                        self.infoLog["Count_WordTokens"] += wordcount
                        if wordcount > 0:
                            line = ','.join(map(str, line))
                            outfile.write(str(line+"\n"))

# CleanCorpus(Corpus="../data/Corpus.txt")



