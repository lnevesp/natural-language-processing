#!/usr/bin/env python

from nltk.tokenize import word_tokenize
import re
import pickle
import html
import pandas as pd
import datetime
import Formats as of


class StupidBackoffP:

    def __init__(self, Sentences, Ngram05, Ngram04, Ngram03, Ngram02, Ngram01, TotalWords):
        self.color01 = "\033[92m"  # Output Color: Green

        StartSB = datetime.datetime.now()

        CleanSentence=self.CleanPhrases(Sentences=Sentences)
        self.findMatch(TrainNgram=CleanSentence,
                       Ngram05=Ngram05, Ngram04=Ngram04, Ngram03=Ngram03, Ngram02=Ngram02, Ngram01=Ngram01,
                       TotalWords=TotalWords)

        TEReadNgram = (datetime.datetime.now() - StartSB)
        print(self.color01 + ">>> " + "\033[0m" + "Time Elapse: " +
              self.color01 + str(round(TEReadNgram.total_seconds(), 2)) + " Seconds" + "\033[0m")

    #TODO: Rewrite into C loop
    def createTokens(self, line):
        words_vector = []  # Creates an empty list
        line = html.unescape(line)  # Removes HTML or XML character references and entities.
        line = [x for x in map(str.strip, line.split('.')) if x]  # Splits  Lines on Period
        line = [x.lower() for x in line]  # Convert to lowercase
        for Sentence in line:
            Sentence = Sentence.strip()  # Deletes the /n on each sentence
            Sentence = ''.join(i for i in Sentence if not i.isdigit())  # Remove numbers
            words = word_tokenize(Sentence)  # Convert lines into word vector (tokenizing)
            # words = self.unusual_words(text=words, vocab=vocab)  # Clean the vocabulary
            words = self.removePunctuation(tokens=words)  # Removes punctuation
            words_vector.append(words)  # Appends the tokens
        return words_vector

    # Remove Punctuation
    def removePunctuation(self, tokens):
        regex = re.compile('[^a-zA-Z]')  # Optimize this thing

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)
        return (words_vector_RP)

    def CleanPhrases(self, Sentences):
        line = self.createTokens(Sentences)
        line = line[0]
        length = len(line)
        previousWords = []
        # Keep only the last 4 words
        if length > 4:
            line = line[-4:]
        else:
            line = line[-length:]
        if line:
            previousWords.append(line)
        return previousWords


    def findMatch(self, TrainNgram, Ngram05, Ngram04, Ngram03, Ngram02, Ngram01, TotalWords):
        TrainNgram = TrainNgram[0]
        length = len(TrainNgram)
        TrainNgram = pd.DataFrame(TrainNgram).T
        labels = ["5Gram", "4Gram", "3Gram", "2Gram"]
        TrainNgram.columns = labels[4-length:]
        columns = ["Candidate", "Score"]
        ScoreData = pd.DataFrame(columns=columns)

        if length > 3:
            result05 = pd.merge(left=TrainNgram, right=Ngram05, on=labels)
            result05["Score"] = result05["Count"] / result05["Count"].sum(axis=0)
            ScoreData=ScoreData.append(result05[columns])
        if length > 2:
            result04 = pd.merge(left=TrainNgram[labels[1:]], right=Ngram04, on=labels[1:])
            result04["Score"] = 0.4*(result04["Count"]/result04["Count"].sum(axis=0))
            ScoreData = ScoreData.append(result04[columns])
        if length > 1:
            result03 = pd.merge(left=TrainNgram[labels[2:]], right=Ngram03, on=labels[2:])
            result03["Score"] = (0.4**2)*(result03["Count"] / result03["Count"].sum(axis=0))
            ScoreData = ScoreData.append(result03[columns])
        if length > 0:
            result02 = pd.merge(left=TrainNgram[labels[3:]], right=Ngram02, on=labels[3:])
            result02["Score"] = (0.4 ** 3) * (result02["Count"] / result02["Count"].sum(axis=0))
            ScoreData = ScoreData.append(result02[columns])

        result01 = Ngram01
        result01["Score"] = (0.4 ** 3) * (result01["Count"] / TotalWords)
        ScoreData = ScoreData.append(result01[columns])

        self.ScoreData = ScoreData.sort_values("Score", ascending=False)
        maxScore = self.ScoreData.groupby(['Candidate']).Score.transform(max)
        self.ScoreData = self.ScoreData[self.ScoreData.Score == maxScore]
        print(self.ScoreData.head(5))


# StupidBackoff("Today is a", Type="user")

