
import StupidBackoff
import pandas as pd
from Formats import TimeFormats as tf

# import os
# os.chdir("/home/lneves/Dropbox/Data Science/University Of Turin/Databases and Algorithms/Algorithms/Project/Version 0.3/python")

class RunStupidBackoff:
    def __init__(self):
        self.color01 = "\033[92m"  # Output Color: Green

        StartReadNgram = tf.calcTimeNow(self)
        tf.timeElapse1(self, time=StartReadNgram, phrase=" Reading Language Model Data")
        temp = pd.read_csv("../data/Ngram-05.csv", iterator=True, chunksize=100000, low_memory=False)
        self.Ngram05 = pd.concat(temp, ignore_index=True)
        temp = pd.read_csv("../data/Ngram-04.csv", iterator=True, chunksize=100000, low_memory=False)
        self.Ngram04 = pd.concat(temp, ignore_index=True)
        temp = pd.read_csv("../data/Ngram-03.csv", iterator=True, chunksize=100000, low_memory=False)
        self.Ngram03 = pd.concat(temp, ignore_index=True)
        temp = pd.read_csv("../data/Ngram-02.csv", iterator=True, chunksize=100000, low_memory=False)
        self.Ngram02 = pd.concat(temp, ignore_index=True)
        self.Ngram01 = pd.read_csv("../data/Ngram-01.csv", low_memory=False)
        TEReadNgram = (tf.formatTime(self, tf.calcTimeNow(self)) -
                       tf.formatTime(self, StartReadNgram))
        tf.timeElapse2(self, TimeElapse=TEReadNgram)

        # Runs Stupid Backoff
        self.runPredict()

    def runPredict(self):
        while True:
            Sentence = input("\n" + self.color01 + ">>> " + "\033[0m" + "Write a sentence (or 'quit()' to exit)" +
                             self.color01 + ": " + "\033[0m")
            if Sentence.strip() == 'quit()':
                break
            else:
                print(self.color01 + ">>> Running Stupid-Backoff Algorithm...")
                StupidBackoff.StupidBackoffP(Sentence, Type="user",
                                             Ngram05=self.Ngram05,
                                             Ngram04=self.Ngram04,
                                             Ngram03=self.Ngram03,
                                             Ngram02=self.Ngram02
                                             )

RunStupidBackoff()