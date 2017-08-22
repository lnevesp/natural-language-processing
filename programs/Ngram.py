import pandas as pd
import sys
from collections import Counter, defaultdict
import Formats as of


# Transform all loops into C Loops
class GenerateNGram:

    def __init__(self, Data, infoLog = defaultdict()):
        self.color01 = "\033[92m"  # Output Color: Green
        self.infoLog = infoLog  # Log Data

        # Print Start Time
        startScript = of.calcTime()
        of.StartScript(time=startScript, phrase="Running Ngram.py")

        """Executes dataModel Function"""
        self.generateNgram(Data)
        self.createNgramData()

        # Print time elapse
        of.EndScript(startScript, "Ngram.py Finished")

    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):

        StartNgram = of.calcTime()
        ngramDict = defaultdict(Counter)
        i = 0
        totalLines = len(TokensData)
        ngramstring = []
        for line in TokensData:
            i += 1
            sys.stdout.write("\r" + self.color01 + " >>>  " + StartNgram + "\033[0m" +
                             " Creating N-Grams" + self.color01 + " | " + "\033[0m" + "Sentence: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100, 2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            line = line.strip().split(',')
            for n in range(1, 6):
                ngrams_counts = Counter(self.CreateNgram(line, n))
                for ngram, count in ngrams_counts.items():
                    string = str('{}\t{}'.format(','.join(ngram), count))
                    ngramstring.append(string)

        print()
        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Counting N-Grams Occurrences")
        for j in ngramstring:
            j = j.strip()
            ngram, count = j.split('\t', 1)
            length = len(ngram.split(','))
            ngram, count = tuple(ngram.split(',')), int(count)
            ngramDict[length][ngram] += count
        of.ElapseEnd(start=StartTime)

        self.infoLog['Time_CreateNGram'] = float(of.deltaTime(StartNgram))

        self.StartFullGram = of.calcTime()  # Save Start Time
        of.ElapseStart(time=self.StartFullGram, phrase="Creating FullGram.csv")

        with open("../data/FullNgrams.csv", 'w') as outfile:
            for length in ngramDict:
                for ngram, count in ngramDict[length].items():
                    line = str('{},{}'.format(','.join(ngram), count))
                    lineCount = line.count(',')
                    completeRow = ',' * (6 - lineCount)
                    line = (str(length) + completeRow + line + "\n")
                    outfile.write(line)

        of.ElapseEnd(start=self.StartFullGram)

    def createNgramData(self):
        StartTime = of.calcTime()  # Save Start Time
        of.ElapseStart(time=StartTime, phrase="Reading FullGram.csv")

        labels = ["NgramID", "5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]  # Columns Names
        Ngrams = [1, 2, 3, 4, 5]  # Ngram types

        tp = pd.read_csv("../data/FullNgrams.csv", names=labels, iterator=True, chunksize=100000, low_memory=False)  # Read File in Chunks
        df = pd.concat(tp, ignore_index=True)  # Join all chunks
        sortOrder = labels[:1] + (list(reversed(labels[1:5]))) + labels[6:]
        df = df.sort_values(sortOrder, ascending=[True, True, True, True, True, False])

        of.ElapseEnd(start=StartTime)

        for i in Ngrams:
            StartTime = of.calcTime()  # Save Start Time
            of.ElapseStart(time=StartTime, phrase="Creating 0" + str(i) + "-Gram Data")
            filename = "../data/Ngram-0" + str(i) + ".csv"
            names = labels[(6 - int(i)):]
            NgramFinal = df.loc[(df.NgramID == i), names]
            NgramFinal = NgramFinal.dropna(axis=0, how='any')
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')
            of.ElapseEnd(start=StartTime)

        self.infoLog['Time_NGramData'] = float(of.deltaTime(self.StartFullGram))