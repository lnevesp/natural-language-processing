from nltk.tokenize import word_tokenize
import re
import pickle
import datetime
import html
import nltk
import sys
import os.path


class CleanCorpus:

    def __init__(self, RawCorpus = "../data/RawCorpus.txt"):
        self.color01 = "\033[92m" # Green
        self.color02 = "\033[93m"  # Yellow
        startCleanData = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + "\n>>> " + "\033[0m" +
              "Starting CleanData.py - " + self.color01 + startCleanData + "\033[0m")

        if os.path.isfile("../data/Tokens.pickle") != 1:

            self.read_corpora(RawCorpus)

            finishCreateTokens = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeElapse = (datetime.datetime.strptime(finishCreateTokens, '%H:%M:%S') -
                          datetime.datetime.strptime(self.startCreateTokens, '%H:%M:%S'))
            print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

            startWriteData = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>>  " + startWriteData + "\033[0m" +
                  " Writing Tokens File", end='', flush=True)
            # If the tokens were created then save then into Tokens.pickle file
            if self.Tokens:
                with open('../data/Tokens.pickle', 'wb') as file:
                    pickle.dump(self.Tokens, file, pickle.HIGHEST_PROTOCOL)
            finishWriteData = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeElapse = (datetime.datetime.strptime(finishWriteData, '%H:%M:%S') -
                          datetime.datetime.strptime(startWriteData, '%H:%M:%S'))
            print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")
        else:
            print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" +
                  " Tokens already created")

        finishCreateCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishCreateCorpus, '%H:%M:%S') -
                      datetime.datetime.strptime(startCleanData, '%H:%M:%S'))
        print(self.color01 + ">>> " + "\033[0m" + "CleanData.py Finished" + self.color01 + " | " + "\033[0m" +
              " Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")


    def createTokens(self, line, vocab):
        words_vector = [] # Creates an empty list
        line = html.unescape(line)  # Removes HTML or XML character references and entities.
        line = [x for x in map(str.strip, line.split('.')) if x]  # Splits  Lines on Period
        line = [x.lower() for x in line]  # Convert to lowercase
        for Sentence in line:
            Sentence = Sentence.strip() # Deletes the /n on each sentence
            Sentence = ''.join(i for i in Sentence if not i.isdigit())  # Remove numbers
            words = word_tokenize(Sentence)  # Convert lines into word vector (tokenizing)
            words = self.unusual_words(text=words, vocab = vocab) # Clean the vocabulary
            words = self.removePunctuation(tokens=words) # Removes punctuation
            words_vector.append(words) # Appends the tokens
        return words_vector

    def unusual_words(self, text, vocab):
        text_vocab = set(w.lower() for w in text if w.isalpha()) # Create a set with the sentence's tokens
        unusual = text_vocab - vocab # Save the words that don't belong to the "english vocabulary"
        Text = text_vocab - unusual # save the words that belong "english vocabulary"
        return Text

    # Remove Punctuation
    def removePunctuation(self, tokens):
        regex = re.compile('[^a-zA-Z]') #

        words_vector_RP = []
        for token in tokens:
            cleanToken = regex.sub('', token)
            if cleanToken:
                words_vector_RP.append(cleanToken)

        return(words_vector_RP)

    """Read the Raw Corpus, returns all sentences tokenized and cleaned"""
    def read_corpora(self, RawCorpus):
        startReading = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>>  " + startReading + "\033[0m" +
              " Reading Corpus", end='', flush=True)
        rawCorpus = open(RawCorpus)
        rawCorpus = rawCorpus.readlines()
        # Print time elapse
        finishReading = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishReading, '%H:%M:%S') -
                      datetime.datetime.strptime(startReading, '%H:%M:%S'))
        print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")


        """Using nltk corpora to built a large corpus of english words"""
        startVocabulary = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>>  " + startVocabulary + "\033[0m" +
              " Creating English Vocabulary Set", end='', flush=True)
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
        finishVocabulary = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishVocabulary, '%H:%M:%S') -
                      datetime.datetime.strptime(startVocabulary, '%H:%M:%S'))
        print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        self.startCreateTokens = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>>  " + self.startCreateTokens + "\033[0m" +
              " Cleaning Data", end='', flush=True)

        self.Tokens = []
        i = 0
        totalLines = len(rawCorpus)
        for line in rawCorpus:
            i += 1
            sys.stdout.write("\r" + self.color01 + ">>>  " + self.startCreateTokens + "\033[0m" +
                             " Cleaning Data" + self.color01 + " | " + "\033[0m" + "Line: " +
                             self.color01 + str(i) + "/" + str(totalLines) +
                             " (" + str(round((i/totalLines)*100,2)) + "%)" + "\033[0m")
            sys.stdout.flush()
            LineToken = self.createTokens(line = line, vocab = english_vocab)
            if LineToken:
                for line in LineToken:
                    self.Tokens.append(line)
        return(self.Tokens)


# CleanCorpus(RawCorpus = "../data/RawCorpus.txt")



