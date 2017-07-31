import glob
import pandas as pd
import Formats as of
import numpy as np


class JoinReduceFiles:

    def __init__(self, DataPath='../data/',  infoLog = pd.DataFrame(np.array([["0001"]]), columns=['ProcessID'])):
        self.infoLog = infoLog
        self.joinReduceOutput(DataPath=DataPath)
        self.createNgramData(DataPath=DataPath)

    def joinReduceOutput(self, DataPath):
        ReduceOutput = glob.glob('../data/MapReduce/*')
        with open(DataPath + "FullNgrams.csv", 'w') as outfile:
            for file in ReduceOutput:
                with open(file) as infile:
                    for line in infile:
                        lineCount = line.count(',')
                        completeRow = ','*(6 - lineCount)
                        line=(str(lineCount) + completeRow + line)
                        outfile.write(line)

    def createNgramData(self, DataPath):
        labels = ["NgramID", "5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]  # Columns Names
        Ngrams = [1, 2, 3, 4, 5]  # Ngram types
        tp = pd.read_csv(DataPath + "FullNgrams.csv", names=labels, iterator=True, chunksize=100000, low_memory=False)  # Read File in Chunks
        df = pd.concat(tp, ignore_index=True)  # Join all chunks
        sortOrder = labels[:1] + (list(reversed(labels[1:5]))) + labels[6:]
        df = df.sort_values(sortOrder, ascending=[True, True, True, True, True, False])
        for i in Ngrams:
            StartTime = of.calcTime()  # Save Start Time
            of.ElapseStart(time=StartTime, phrase="Creating 0" + str(i) + "-Gram Data")
            # print("Creating 0" + str(i))
            filename = "../data/Ngram-0" + str(i) + ".csv"
            names = labels[(6 - int(i)):]
            NgramFinal = df.loc[(df.NgramID == i), names]
            if len(names) == 2:
                NgramFinal = NgramFinal.head(5)
            NgramFinal = NgramFinal.dropna(axis=0, how='any')
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')
            of.ElapseEnd(start=StartTime)


# JoinReduceFiles(DataPath='../data/')