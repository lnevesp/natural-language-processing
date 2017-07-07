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
        # self.dataModel(Data)
        self.generateNgram(Data)
        self.createNgramData()

        # Print time elapse
        self.infoLog['TENgramScript'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                         tf.formatTime(self, startNgram))
        tf.StopScript(self, TimeElapse=self.infoLog['TENgramScript'], phrase="Ngram.py Finished")


    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):

        self.StartNgram = tf.calcTimeNow(self)
        ngramDict = defaultdict(Counter)
        i = 0
        totalLines = len(TokensData)
        ngramstring = []
        for line in TokensData:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.StartNgram + "\033[0m" +
                             " Creating N-Grams" + self.color01 + " | " + "\033[0m" + "Sentence: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100,2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            for n in range(1, 6):
                ngrams_counts = Counter(self.CreateNgram(line, n))
                for ngram, count in ngrams_counts.items():
                    string = str('{}\t{}'.format(','.join(ngram), count))
                    ngramstring.append(string)

        print("\n" + self.color01 + ">>> " + "\033[0m" + "Summing N-Grams Occurrences")
        for j in ngramstring:
            j = j.strip()
            ngram, count = j.split('\t', 1)
            length = len(ngram.split(','))
            ngram, count = tuple(ngram.split(',')), int(count)
            ngramDict[length][ngram] += count

        StartFullGram = tf.calcTimeNow(self)  # Save Start Time
        tf.timeElapse1(self, time=StartFullGram, phrase="Creating FullGram.csv")

        with open("../data/FullNgrams.csv", 'w') as outfile:
            outline = []
            for length in ngramDict:
                for ngram, count in ngramDict[length].items():
                    line = str('{},{}'.format(','.join(ngram), count))
                    lineCount = line.count(',')
                    completeRow = ',' * (6 - lineCount)
                    line = (str(length) + completeRow + line + "\n")
                    outfile.write(line)
            # for line in outline:
            #     outfile.write(line)


        TEFullGram = (tf.formatTime(self, tf.calcTimeNow(self)) -
                      tf.formatTime(self, StartFullGram))
        tf.timeElapse2(self, TimeElapse=TEFullGram)


    def createNgramData(self):
        labels = ["NgramID", "5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]  # Columns Names
        Ngrams = [1, 2, 3, 4, 5]  # Ngram types

        StartReadFullGram = tf.calcTimeNow(self)  # Save Start Time
        tf.timeElapse1(self, time=StartReadFullGram, phrase="Reading FullGram.csv")

        tp = pd.read_csv("../data/FullNgrams.csv", names=labels, iterator=True, chunksize=100000, low_memory=False)  # Read File in Chunks
        df = pd.concat(tp, ignore_index=True)  # Join all chunks
        sortOrder = labels[:1] + (list(reversed(labels[1:5]))) + labels[6:]
        df = df.sort_values(sortOrder, ascending=[True, True, True, True, True, False])

        TEReadFullGram = (tf.formatTime(self, tf.calcTimeNow(self)) -
                      tf.formatTime(self, StartReadFullGram))
        tf.timeElapse2(self, TimeElapse=TEReadFullGram)

        for i in Ngrams:
            StartWriteNgram = tf.calcTimeNow(self)  # Save Start Time
            tf.timeElapse1(self, time=StartWriteNgram, phrase="Creating 0" + str(i) + "-Gram Data")
            filename = "../data/Ngram-0" + str(i) + ".csv"
            names = labels[(6 - int(i)):]
            NgramFinal = df.loc[(df.NgramID == i), names]
            if len(names) == 2:
                NgramFinal = NgramFinal.head(5)
            NgramFinal = NgramFinal.dropna(axis=0, how='any')
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')
            TECreateNgram = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                 tf.formatTime(self, StartWriteNgram))
            tf.timeElapse2(self, TimeElapse=TECreateNgram)
