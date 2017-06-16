from nltk.tokenize import word_tokenize
import re
import string
import pickle


class CleanCorpus:

    def __init__(self, RawCorpus = "../data/RawCorpus.txt"):
        self.RawCorpus = "../data/RawCorpus.txt"
        self.read_corpora(RawCorpus)
        if self.Tokens:
            with open('../data/Tokens.txt', 'wb') as file:
                pickle.dump(self.Tokens, file)

    def createTokens(self, line):
        line = line.strip() # strip /n
        line = line.lower() # Convert to lowercase
        line = ''.join(i for i in line if not i.isdigit()) # Remove numbers
        words_vector = word_tokenize(line) # Convert lines into word vector (tokenizing)
        words_vector = self.removePunctuation(tokens=words_vector)
        return words_vector[0]

    def removePunctuation(self, tokens):
        regex = re.compile('[%s]' % re.escape(string.punctuation))

        words_vector_RP = []
        new_review = []
        for token in tokens:
            new_token = regex.sub(u'', token)
            if not new_token == u'':
                new_review.append(new_token)
        words_vector_RP.append(new_review)
        return(words_vector_RP)

    def read_corpora(self, RawCorpus):
        """Read the Raw Corpus, returns a list (sentence) of list(words) of lists(alternatives).
                   The first item in each word list is the correct word."""
        rawCorpus = open(RawCorpus)
        self.Tokens = []
        for line in rawCorpus:
            LineToken = self.createTokens(line)
            if LineToken:
                self.Tokens.append(LineToken)
        return(self.Tokens)

CleanCorpus(RawCorpus = "../data/RawCorpus.txt")