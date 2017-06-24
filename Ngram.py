import pandas as pd
import pickle
from collections import Counter, defaultdict
from time import gmtime, strftime


class GenerateNGram:

    def __init__(self, DataPath = "../data/Tokens.txt"):
        print("Iniciated at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.DataPath = DataPath
        with open('../data/Tokens.pickle', "rb") as file:  # Unpickling
            self.TokensData = pickle.load(file)
        self.dataModel()

    def CreateNgram(self, TokensData, n):
        return zip(*[TokensData[i:] for i in range(n)])

    def generateNgram(self, TokensData):
        ngramDict = defaultdict(list)
        for line in TokensData:
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
        labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate", "Count"]
        Ngram = ['1', '2', '3', '4', '5']
        for i in Ngram:
            NgramFinal = pd.DataFrame(OutNgramDict[str(i)], columns=labels[(5 - int(i)):])
            filename = "../data/Ngram" + str(i) + ".csv"
            NgramFinal.to_csv(filename, index=False, encoding='utf-8')
        print("Finished at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

GenerateNGram(DataPath = "../data/Tokens.txt")


