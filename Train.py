from DownloadFile import CreateCorpus
import StupidBackoff
import CleanCorpus



def main():

    # Download and create corpus
    CreateCorpus()

    # Iniciate Data Cleaning and Ngrams Generation
    trainPath = './data/Corpus.txt'
    CleanCorpus().read_corpora(trainPath)

    # Iniciate Stupid Backoff
    Sentence = input("Write a sentence: ")
    print(Sentence)
    print('Stupid Backoff: ')
    SBResult = StupidBackoff(Sentence)
    print(SBResult)