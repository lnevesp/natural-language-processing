import pandas as pd
import sys
import datetime
from collections import Counter, defaultdict


class GenerateNGram:

    def __init__(self, Data):
        self.color01 = "\033[92m" # Green
        self.color02 = "\033[93m"  # Yellow

        startGenerateNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + "\n>>> " + "\033[0m" +
              "Starting Ngram.py - " + self.color01 + startGenerateNgram + "\033[0m")

        print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" + " Reading Tokens Sample")
        self.TokensData = Data
        self.dataModel()

        finishGenerateNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishGenerateNgram, '%H:%M:%S') -
                      datetime.datetime.strptime(startGenerateNgram, '%H:%M:%S'))
        print(self.color01 + ">>> " + "\033[0m" + "Ngram.py Finished" + self.color01 + " | " + "\033[0m" +
              "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):
        self.startNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        ngramDict = defaultdict(list)
        i = 0
        totalLines = len(TokensData)
        for line in TokensData:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.startNgram + "\033[0m" +
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
        return ngramDict

    def dataModel(self):
        OutNgramDict = self.generateNgram(TokensData=self.TokensData)
        finishNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishNgram, '%H:%M:%S') -
                      datetime.datetime.strptime(self.startNgram, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 +str(TimeElapse) + "\033[0m")
        labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]
        Ngram = ['1', '2', '3', '4', '5']
        for i in Ngram:
            startwrite = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>>  " + startwrite + "\033[0m" +
                  " Creating 0" + i + "-Gram Data", end='', flush=True)
            NgramFinal = pd.DataFrame(OutNgramDict[str(i)], columns=labels[(5 - int(i)):])
            filename = "../data/Ngram" + str(i) + ".csv"
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')
            finishwrite = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeElapse = (datetime.datetime.strptime(finishwrite, '%H:%M:%S') -
                          datetime.datetime.strptime(startwrite, '%H:%M:%S'))
            print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")