import pandas as pd
import sys
import datetime
from collections import Counter, defaultdict
from Formats import TimeFormats


class GenerateNGram:

    def __init__(self, Data, infoLog = defaultdict()):
        self.color01 = "\033[92m"  # Green
        self.infoLog = infoLog  # Log Data


        startNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.StartScript(self, time=startNgram, phrase="Starting Ngram.py")

        # print(self.color01 + "\n>>> " + "\033[0m" +
        #       "Starting Ngram.py - " + self.color01 + startGenerateNgram + "\033[0m")

        StartReadSample = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.timeElapse1(self, time=StartReadSample, phrase="Reading Sample")
        # print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" + " Reading Tokens Sample")
        self.TokensData = Data
        # Print time elapse
        StopReadSample = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEReadSample'] = (datetime.datetime.strptime(StopReadSample, '%H:%M:%S') -
                                         datetime.datetime.strptime(StartReadSample, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEReadSample'])

        self.dataModel()

        # Print time elapse
        StopNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TENgramScript'] = (datetime.datetime.strptime(StopNgram, '%H:%M:%S') -
                                         datetime.datetime.strptime(startNgram, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TENgramScript'])
        # finishGenerateNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        # TimeElapse = (datetime.datetime.strptime(finishGenerateNgram, '%H:%M:%S') -
        #               datetime.datetime.strptime(startGenerateNgram, '%H:%M:%S'))
        # print(self.color01 + ">>> " + "\033[0m" + "Ngram.py Finished" + self.color01 + " | " + "\033[0m" +
        #       "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):
        self.StartLineNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        ngramDict = defaultdict(list)
        i = 0
        totalLines = len(TokensData)
        for line in TokensData:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.StartLineNgram + "\033[0m" +
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
        # Create Ngrams for each line
        OutNgramDict = self.generateNgram(TokensData=self.TokensData)

        StopLineNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TELineNgram'] = (datetime.datetime.strptime(StopLineNgram, '%H:%M:%S') -
                                         datetime.datetime.strptime(self.StartLineNgram, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TELineNgram'])

        #
        # finishNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
        # TimeElapse = (datetime.datetime.strptime(finishNgram, '%H:%M:%S') -
        #               datetime.datetime.strptime(self.startNgram, '%H:%M:%S'))
        # print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 +str(TimeElapse) + "\033[0m")

        labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]
        Ngram = ['1', '2', '3', '4', '5']
        for i in Ngram:

            StartWriteNgram = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=StartWriteNgram, phrase=" Creating 0" + i + "-Gram Data")

            # startwrite = datetime.datetime.now().time().strftime('%H:%M:%S')
            # print(self.color01 + ">>>  " + startwrite + "\033[0m" +
            #       " Creating 0" + i + "-Gram Data", end='', flush=True)
            NgramFinal = pd.DataFrame(OutNgramDict[str(i)], columns=labels[(5 - int(i)):])
            filename = "../data/Ngram" + str(i) + ".csv"
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')

            # Print time elapse
            key = "TE0" + i + "Gram"
            StopWriteCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog[key] = (datetime.datetime.strptime(StopWriteCorpus, '%H:%M:%S') -
                                 datetime.datetime.strptime(StartWriteNgram, '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog[key])


            # finishwrite = datetime.datetime.now().time().strftime('%H:%M:%S')
            # TimeElapse = (datetime.datetime.strptime(finishwrite, '%H:%M:%S') -
            #               datetime.datetime.strptime(startwrite, '%H:%M:%S'))
            # print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")