#!/usr/bin/env python

from nltk.tokenize import word_tokenize
import re
import pickle
import html
import pandas as pd
import datetime


class StupidBackoffP:

    def __init__(self, Sentences, Type, Ngram05, Ngram04, Ngram03, Ngram02):
        self.color01 = "\033[92m"  # Output Color: Green

        StartSB = datetime.datetime.now()
        self.Ngram05=Ngram05
        self.Ngram04 = Ngram04
        self.Ngram03 = Ngram03
        self.Ngram02 = Ngram02

        CleanSentence=self.CleanPhrases(Sentences=Sentences, Type=Type)
        self.findMatch(TrainNgram=CleanSentence, Type="user",
                       Ngram05 = self.Ngram05,
                       Ngram04 = self.Ngram04,
                       Ngram03 = self.Ngram03,
                       Ngram02 = self.Ngram02)
        TEReadNgram = (datetime.datetime.now() - datetime.datetime.now())
        print(self.color01 + ">>> " + "\033[0m" + "Time Elapse: " + str(TEReadNgram.total_seconds() * 1000))


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
        regex = re.compile('[^a-zA-Z]')

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)
        return (words_vector_RP)

    def CleanPhrases(self, Sentences, Type):
        if Type == "test":
            with open(Sentences, "rb") as file:  # Unpickling
                TestData = pickle.load(file)
                previousWords = []
                for line in TestData:
                    length = len(line)
                    if length > 5:
                        line=line[-5:]
                    else:
                        line=line[-length:]
                    if line:
                        previousWords.append(line)
            return previousWords
        elif Type == "user":
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


    def findMatch(self, TrainNgram, Type, Ngram05, Ngram04, Ngram03, Ngram02):
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

        self.ScoreData = ScoreData.sort_values("Score", ascending=False)
        maxScore = self.ScoreData.groupby(['Candidate']).Score.transform(max)
        self.ScoreData = self.ScoreData[self.ScoreData.Score == maxScore]
        print(self.ScoreData.head(5))


# StupidBackoff("Today is a", Type="user")

