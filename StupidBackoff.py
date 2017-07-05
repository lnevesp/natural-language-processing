import collections
import math
# from CleanData import CleanCorpus
import pandas as pd


class StupidBackoff:

    def __init__(self, Phrase, ):
        self.NgramDict()
    # TODO: Read sys.arg[]
    def createTokens(self, line):
        line = line.strip()  # strip /n
        line = line.lower()  # Convert to lowercase
        line = ''.join(i for i in line if not i.isdigit())  # Remove numbers
        words_vector = word_tokenize(line)  # Convert lines into word vector (tokenizing)
        words_vector = self.removePunctuation(tokens=words_vector)
        return words_vector[0]

    # Remove Punctuation
    def removePunctuation(self, tokens):
        regex = re.compile("/^[a-zA-Z]+$/")
        words_vector_RP = []
        # new_review = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            words_vector_RP.append(cleanToken)
        return (words_vector_RP)

    def CleanPhrase(self, inputPhrase):
        cleanTokens = self.createTokens(inputPhrase)
        n = len(cleanTokens)
        if n >= 4:
            self.lastWords = cleanTokens[(len(cleanTokens)-4):]
        else:
            self.lastWords = cleanTokens[:]


    def StupidBackoff(self, input):
        inputNgram = self.CleanPhrase(inputPhrase = input)
        n = len(inputNgram)
        labels = ["5Gram", "4Gram", "3Gram", "2Gram"]
        inputNgram = pd.DataFrame(inputNgram, columns=labels[(4-n):])
        for i in list(range(n+1,1,-1)):
            pd.merge(left=self.NgramDict[[i]], right=inputNgram)





    def __init__(self, corpus):
        self.NGram01 = collections.defaultdict(lambda: 0)
        self.NGram02 = collections.defaultdict(lambda: 0)
        self.NGram03 = collections.defaultdict(lambda: 0)
        self.NGram04 = collections.defaultdict(lambda: 0)
        self.NGram05 = collections.defaultdict(lambda: 0)
        self.total = 0
        self.vocab_size = 0
        self.train(corpus)

    def train(self, corpus):
        # Unigram counts
        for sentence in corpus.corpus:
            for datum in sentence.data:
                token = datum.word
                self.NGram01[token] += 1
                self.total += 1
        self.vocab_size = len(self.NGram01)
        # Bigram counts
        for sentence in corpus.corpus:
            if len(sentence) <= 1:
                continue
            previous = sentence.data[0].word
            for datum in sentence.data[1:]:
                token = datum.word
                self.NGram02[(previous, token)] += 1
                previous = token
        # Trigram counts
        for sentence in corpus.corpus:
            if len(sentence) <= 2:
                continue
            previous = sentence.data[0].word
            for datum in sentence.data[1:]:
                token = datum.word
                self.NGram03[(previous, token)] += 1
                previous = token
        # 4-Gram counts
        for sentence in corpus.corpus:
            if len(sentence) <= 3:
                continue
            previous = sentence.data[0].word
            for datum in sentence.data[1:]:
                token = datum.word
                self.NGram04[(previous, token)] += 1
                previous = token
        # 5-Gram counts
        for sentence in corpus.corpus:
            if len(sentence) <= 4:
                continue
            previous = sentence.data[0].word
            for datum in sentence.data[1:]:
                token = datum.word
                self.NGram05[(previous, token)] += 1
                previous = token


    def score(self, sentence):
        score = 0.0
        previous = sentence[0]
        for token in sentence[1:]:
            Count05 = self.NGram02[(previous, token)]
            Count05_ = self.NGram01[previous]
            unicount = self.NGram01[token]
            if Count05 > 0:
                score += math.log(Count05)
                score -= math.log(Count05_)
            elif Count04 > 0:
                score += math.log(0.4)
                score += math.log(Count04 + 1)
                score -= math.log(self.total + self.vocab_size)
            elif Count03 > 0:
                score += math.log(0.4)**2
                score += math.log(Count03 + 1)
                score -= math.log(self.total + self.vocab_size)
            elif Count02 > 0:
                score += math.log(0.4)**3
                score += math.log(Count02 + 1)
                score -= math.log(self.total + self.vocab_size)
            else:
                score += math.log(0.4)**4
                score += math.log(unicount + 1)
                score -= math.log(self.total + self.vocab_size)
            previous = token
        return score

