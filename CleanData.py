from nltk.tokenize import word_tokenize
import re
import pickle
import datetime
import html
import nltk
import sys
import os.path
from Formats import TimeFormats
from collections import defaultdict


class CleanCorpus:

    def __init__(self, RawCorpus = "../data/RawCorpus.txt", infoLog = defaultdict()):
        self.color01 = "\033[92m"  # Green
        self.infoLog = infoLog

        StartCleanScript = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.StartScript(self, time=StartCleanScript, phrase="Starting CleanData.py")

        if os.path.isfile("../data/Tokens.pickle") != 1:

            self.read_corpora(RawCorpus)

            StopCleanLines = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TECleanLines'] = (datetime.datetime.strptime(StopCleanLines, '%H:%M:%S') -
                                            datetime.datetime.strptime(StartCleanScript, '%H:%M:%S'))
            TimeFormats.timeElapse2(self, self.infoLog['TECleanLines'])

            StartWriteTokens = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=StartWriteTokens, phrase="Writing Tokens File")

            # If the tokens were created then save then into Tokens.pickle file
            if self.Tokens:
                with open('../data/Tokens.pickle', 'wb') as file:
                    pickle.dump(self.Tokens, file, pickle.HIGHEST_PROTOCOL)
            # Print time elapse
            StopWriteTokens = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEWriteTokens'] = (datetime.datetime.strptime(StopWriteTokens, '%H:%M:%S') -
                                          datetime.datetime.strptime(StartWriteTokens, '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEWriteTokens'])

        else:
            TimeFormats.NormalMessage(self, phrase="Tokens already created")
            self.infoLog['TEWriteTokens'] = datetime.timedelta(0)

        # Print Final Time
        StopCleanScript = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TECleanScript'] = (datetime.datetime.strptime(StopCleanScript, '%H:%M:%S') -
                                         datetime.datetime.strptime(StartCleanScript, '%H:%M:%S'))
        TimeFormats.StopScript(self, TimeElapse=self.infoLog['TECleanScript'], phrase="CleanData.py Finished")


    def createTokens(self, line, vocab):
        words_vector = []  # Creates an empty list
        line = html.unescape(line)  # Removes HTML or XML character references and entities.
        line = [x for x in map(str.strip, line.split('.')) if x]  # Splits  Lines on Period
        line = [x.lower() for x in line]  # Convert to lowercase
        for Sentence in line:
            Sentence = Sentence.strip()  # Deletes the /n on each sentence
            Sentence = ''.join(i for i in Sentence if not i.isdigit())  # Remove numbers
            words = word_tokenize(Sentence)  # Convert lines into word vector (tokenizing)
            words = self.unusual_words(text=words, vocab=vocab)  # Clean the vocabulary
            words = self.removePunctuation(tokens=words)  # Removes punctuation
            words_vector.append(words)  # Appends the tokens
        return words_vector

    def unusual_words(self, text, vocab):
        text_vocab = set(w.lower() for w in text if w.isalpha())  # Create a set with the sentence's tokens
        unusual = text_vocab - vocab  # Save the words that don't belong to the "english vocabulary"
        Text = text_vocab - unusual  # save the words that belong "english vocabulary"
        return Text

    # Remove Punctuation
    def removePunctuation(self, tokens):
        regex = re.compile('[^a-zA-Z]')

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)

        return(words_vector_RP)

    """Read the Raw Corpus, returns all sentences tokenized and cleaned"""
    def read_corpora(self, RawCorpus):
        # Print start download time
        startReadingCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.timeElapse1(self, time=startReadingCorpus, phrase="Reading Corpus")

        rawCorpus = open(RawCorpus)
        rawCorpus = rawCorpus.readlines()

        # Print time elapse
        stopReadingCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEReadCorpus'] = (datetime.datetime.strptime(stopReadingCorpus, '%H:%M:%S') -
                                      datetime.datetime.strptime(startReadingCorpus, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEReadCorpus'])


        """Using nltk corpora to built a large corpus of english words"""

        startVocabulary = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.timeElapse1(self, time=startVocabulary, phrase="Creating English Vocabulary Set")

        english_vocab = set(w.lower() for w in nltk.corpus.brown.words())
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.reuters.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.words.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.abc.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.genesis.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.gutenberg.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.state_union.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.webtext.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.names.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.movie_reviews.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.wordnet.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.treebank.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.stopwords.words()))
        english_vocab = english_vocab.union(set(w.lower() for w in nltk.corpus.state_union.words()))

        # Print time elapse
        stopVocabulary = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEVocabulary'] = (datetime.datetime.strptime(stopVocabulary, '%H:%M:%S') -
                                        datetime.datetime.strptime(startVocabulary, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEVocabulary'])


        self.infoLog['StartCleanLines'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.Tokens = []
        i = 0
        totalLines = len(rawCorpus)
        for line in rawCorpus:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.infoLog['StartCleanLines'] + "\033[0m" +
                             " Cleaning Data" + self.color01 + " | " + "\033[0m" + "Line: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100,2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            LineToken = self.createTokens(line=line, vocab=english_vocab)
            if LineToken:
                for line in LineToken:
                    self.Tokens.append(line)
        return(self.Tokens)


# CleanCorpus(RawCorpus = "../data/RawCorpus.txt")



