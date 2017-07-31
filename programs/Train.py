import StupidBackoff
import pandas as pd
import Formats as of
import os
import numpy as np


class RunStupidBackoff:
    def __init__(self):
        self.color01 = "\033[92m"  # Output Color: Green
        self.infoLog = pd.DataFrame(np.array([["0001",]]), columns=['ProcessID'])

        StartReadNgram = of.calcTime()
        of.ElapseStart(time=StartReadNgram, phrase="Reading N-Gram Data")
        self.Ngram05 = self.readNgram(Ngram=5)
        self.Ngram04 = self.readNgram(Ngram=4)
        self.Ngram03 = self.readNgram(Ngram=3)
        self.Ngram02 = self.readNgram(Ngram=2)
        self.Ngram01 = self.readNgram(Ngram=1)
        of.ElapseEnd(StartReadNgram)

        for i in range(1,6):
            varName = 'FileSize_Ngram-0' + str(i)
            self.infoLog[varName] = round(os.path.getsize("../data/Ngram-0" + str(i) + ".csv") / (1024 * 1024.0), 2)

        # Runs Stupid Backoff
        self.runPredict()

        print(self.infoLog)

    def readNgram(self, Ngram):
        temp = pd.read_csv("../data/Ngram-0" + str(Ngram) + ".csv", iterator=True, chunksize=100000, low_memory=False)
        temp = pd.concat(temp, ignore_index=True)
        return temp

    def runPredict(self):
        while True:
            Sentence = input("\n" + self.color01 + ">>> " + "\033[0m" + "Write a sentence (or 'quit()' to exit)" +
                             self.color01 + ": " + "\033[0m" + "\n" + self.color01 + ">>> \t" + "\033[0m")
            if Sentence.strip() == 'quit()':
                break
            else:
                print(self.color01 + ">>> Running Stupid-Backoff Algorithm..." + "\033[0m" + "\n")
                StupidBackoff.StupidBackoffP(Sentence, Type="user",
                                             Ngram05=self.Ngram05,
                                             Ngram04=self.Ngram04,
                                             Ngram03=self.Ngram03,
                                             Ngram02=self.Ngram02
                                             )

RunStupidBackoff()