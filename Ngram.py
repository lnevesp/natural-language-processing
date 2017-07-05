import pandas as pd
import sys
from collections import Counter, defaultdict
from Formats import TimeFormats as tf


class GenerateNGram:

    def __init__(self, Data, infoLog = defaultdict()):
        self.color01 = "\033[92m"  # Output Color: Green
        self.infoLog = infoLog  # Log Data

        # Print Start Time
        startNgram = tf.calcTimeNow(self)
        tf.StartScript(self, time=startNgram, phrase="Starting Ngram.py")

        """Executes dataModel Function"""
        self.dataModel(Data)

        # Print time elapse
        self.infoLog['TENgramScript'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                         tf.formatTime(self, startNgram))
        tf.StopScript(self, TimeElapse=self.infoLog['TENgramScript'], phrase="Ngram.py Finished")


    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):
        self.StartNgram = tf.calcTimeNow(self)
        ngramDict = defaultdict(list)
        i = 0
        totalLines = len(TokensData)
        for line in TokensData:
            ngrams_counts = defaultdict(list)
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.StartNgram + "\033[0m" +
                             " Creating N-Grams" + self.color01 + " | " + "\033[0m" + "Sentence: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100,2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            for n in range(1, 6):
                ngrams_counts = Counter(self.CreateNgram(line, n))
            for ngram, count in ngrams_counts.items():
                length = len(ngram)
                ngramList = list(ngram)
                ngramList.append(str(count))
                ngramDict[str(length)].append(ngramList)
                # TODO: sum count. (copy from JoinReduce.py)
        return ngramDict


    def dataModel(self, Data):
        """Reads Sample Train Data and Print Times"""

        StartReadSample = tf.calcTimeNow(self)   # Save Start Time
        tf.timeElapse1(self, time=StartReadSample, phrase="Reading Sample")   # Print Start Reading Sample

        TokensData = Data  # Read Sample Train Data

        # StopReadSample = tf.calcTimeNow(self)
        self.infoLog['TEReadSample'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                        tf.formatTime(self, StartReadSample))  # Calculate time elapse
        tf.StopScript(self, TimeElapse=self.infoLog['TEReadSample'], phrase="Ngram.py Finished")  # Print time elapse

        ################################################################
        """Create Ngrams for each line"""
        OutNgramDict = self.generateNgram(TokensData=TokensData)

        self.infoLog['TELineNgram'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                       tf.formatTime(self, self.StartNgram))  # Calculate time elapse
        tf.timeElapse2(self, TimeElapse=self.infoLog['TELineNgram'])  # Print time elapse (End of Print)

        ################################################################
        """Separate Ngrams into 5 Datasets"""
        labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]  # Columns Names
        Ngram = ['1', '2', '3', '4', '5']  # Ngram types

        for i in Ngram:

            StartWriteNgram = tf.calcTimeNow(self)
            tf.timeElapse1(self, time=StartWriteNgram, phrase=" Creating 0" + i + "-Gram Data")

            NgramFinal = pd.DataFrame(OutNgramDict[str(i)], columns=labels[(5 - int(i)):])
            filename = "../data/Ngram" + str(i) + ".csv"
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')

            # Print time elapse
            key = "TE0" + i + "Gram"
            # StopWriteCorpus = tf.calcTimeNow(self)
            self.infoLog[key] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                 tf.formatTime(self, StartWriteNgram))
            tf.timeElapse2(self, TimeElapse=self.infoLog[key])

