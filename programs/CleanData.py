from nltk.tokenize import word_tokenize
import re
import pickle
import datetime
import html
import sys
import os.path
from Formats import TimeFormats as tf
from collections import defaultdict


class CleanCorpus:

    def __init__(self, RawCorpus = "../data/RawCorpus.txt", infoLog = defaultdict()):
        self.color01 = "\033[92m"  # Green
        self.infoLog = infoLog  # Log Dataframe

        StartCleanScript = tf.calcTimeNow(self)  # Save start script time
        tf.StartScript(self, time=StartCleanScript, phrase="Starting CleanData.py")  # Print start time

        if os.path.isfile("../data/Tokens.pkl") != 1:  # Check if the file already exists

            self.read_corpora(RawCorpus)  # Read Raw Corpus

            self.infoLog['TECleanLines'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                            tf.formatTime(self, StartCleanScript))  # Calculate Time Elapse
            tf.timeElapse2(self, self.infoLog['TECleanLines'])  # Print time Elapse

            StartWriteTokens = tf.calcTimeNow(self)
            tf.timeElapse1(self, time=StartWriteTokens, phrase="Writing Tokens File")

            # If the tokens were created then save then into Tokens.pickle file
            if self.Tokens:
                with open('../data/Tokens.pkl', 'wb') as file:
                    pickle.dump(self.Tokens, file, pickle.HIGHEST_PROTOCOL)
            # Print time elapse
            # StopWriteTokens = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEWriteTokens'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                             tf.formatTime(self, StartWriteTokens))
            tf.timeElapse2(self, TimeElapse=self.infoLog['TEWriteTokens'])

        else:
            tf.NormalMessage(self, phrase="Tokens already created")
            self.infoLog['TEWriteTokens'] = datetime.timedelta(0)

        # Print Final Time
        # StopCleanScript = tf.calcTimeNow(self)
        self.infoLog['TECleanScript']=(tf.formatTime(self, tf.calcTimeNow(self))-tf.formatTime(self, StartCleanScript))
        tf.StopScript(self, TimeElapse=self.infoLog['TECleanScript'], phrase="CleanData.py Finished")

    # Remove Punctuation
    def removePunctuation(self, tokens):
        regex = re.compile('[^a-zA-Z]')

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)
        return(words_vector_RP)

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

    """Read the Raw Corpus, returns all sentences tokenized and cleaned"""
    def read_corpora(self, RawCorpus):
        # Print start download time
        startReadingCorpus = tf.calcTimeNow(self)
        tf.timeElapse1(self, time=startReadingCorpus, phrase="Reading Corpus")

        rawCorpus = open(RawCorpus)
        rawCorpus = rawCorpus.readlines()

        # Print time elapse
        self.infoLog['TEReadCorpus'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                        tf.formatTime(self,startReadingCorpus))
        tf.timeElapse2(self, TimeElapse=self.infoLog['TEReadCorpus'])


        self.infoLog['StartCleanLines'] = tf.calcTimeNow(self)
        self.Tokens = []
        i = 0
        totalLines = len(rawCorpus)
        for line in rawCorpus:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.infoLog['StartCleanLines'] + "\033[0m" +
                             " Cleaning Data" + self.color01 + " | " + "\033[0m" + "Line: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100,2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            # LineToken = self.createTokens(line=line, vocab=english_vocab)
            LineToken = self.createTokens(line=line)
            if LineToken:
                for line in LineToken:
                    self.Tokens.append(line)
        return(self.Tokens)


# CleanCorpus(RawCorpus="../data/RawCorpus.txt")



