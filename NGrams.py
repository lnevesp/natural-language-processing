import pandas as pd
import pickle


class GenerateNGram:

    def __init__(self, DataPath = "../data/Tokens.txt"):
        self.DataPath = "../data/Tokens.txt"
        self.dataModel()

    def createNgrams(self, TokensData, NgramType):
        # Set columns names
        labels = ["5Gram", "4Gram", "3Gram", "2Gram", "Candidate"]
        Ngram = pd.DataFrame(columns=labels[(5-NgramType):])
        # Create Ngram
        for TokenLine in TokensData:
            if len(TokenLine) >= NgramType:
                ngramTemp = list(zip(*[TokenLine[i:] for i in range(NgramType)]))
                ngramTemp = pd.DataFrame.from_records(ngramTemp, columns=labels[(5-NgramType):])
                frame = [Ngram, ngramTemp]
                Ngram = pd.concat(frame)
            Ngram = Ngram.reset_index(drop=True)
        # Count Ngrams
        Ngram = Ngram.groupby(Ngram.columns.tolist()).size().reset_index().rename(columns={0: 'Count'})
        Ngram = Ngram.sort(['Count'], ascending = False)
        return Ngram

    def dataModel(self):
        with open(self.DataPath, "rb") as file:  # Unpickling
            self.TokensData = pickle.load(file)
        for Ngram in list(range(2, 6)):
            OutNgram = self.createNgrams(TokensData = self.TokensData, NgramType = Ngram)
            filename = "../data/Ngram" + str(Ngram) + ".csv"
            OutNgram.to_csv(filename, index=False, encoding='utf-8')

GenerateNGram(DataPath = "../data/Tokens.txt")
