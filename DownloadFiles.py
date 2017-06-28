import urllib.request
import tarfile
import os.path
import glob
import datetime


class CreateCorpus:

    def __init__(self, DataPath = '../data/'):
        self.color01 = "\033[92m" # Green
        self.color02 = "\033[93m"  # Yellow
        startCreateCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + "\n>>> " + "\033[0m" +
              "Starting DownloadFiles.py - " + self.color01 + startCreateCorpus + "\033[0m")
        self.DataPath = '../data/'
        self.downloadFiles(DataPath)
        self.extractFiles(self.DataPath)
        self.createCorpus(self.DataPath)
        finishCreateCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishCreateCorpus, '%H:%M:%S') -
                      datetime.datetime.strptime(startCreateCorpus, '%H:%M:%S'))
        print(self.color01 + ">>> " + "\033[0m" +
              "DownloadFiles.py Finished" + self.color01 + " | " + "\033[0m" +
              "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    # Check if the files are already downloaded, if not it download it
    def downloadFiles(self, DataPath):

        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:
            startdownload = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>>  " + startdownload + "\033[0m" +
                  " Downloading Corpora", end='', flush=True)
            # Downloading Corpora
            urllib.request.urlretrieve("https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1",
                                       DataPath + "ANC_Corpora.tar.gz")
            # Print time elapse
            finishdownload = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeElapse = (datetime.datetime.strptime(finishdownload, '%H:%M:%S') -
                          datetime.datetime.strptime(startdownload, '%H:%M:%S'))
            print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        else:
            print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" +
                  " Corpora already downloaded")

    # Extract files function
    def extractFunction(self, tar_url, DataPath):
        startextract = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>>  " + startextract + "\033[0m" +
              " Extract Corpora", end='', flush=True)
        tar = tarfile.open(tar_url, 'r')
        for item in tar:
            tar.extract(item, DataPath )
            if item.name.find(".tar.gz") != -1:
                extractFunction(item.name, "./" + item.name[:item.name.rfind('/')])
        # Print time elapse
        finishextract = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishextract, '%H:%M:%S') -
                      datetime.datetime.strptime(startextract, '%H:%M:%S'))
        print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    # Check if the files are already extracted, if not then do the extraction...
    def extractFiles(self, DataPath):
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractFunction(DataPath + "ANC_Corpora.tar.gz", DataPath = "../data/")
        else:
            print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" +
                  " Files already extracted")

    # Aggregate Files
    def createCorpus(self, DataPath):
        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')
        if os.path.isfile(DataPath + "RawCorpus.txt") != 1:
            startcorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>>  " + startcorpus + "\033[0m" +
                  " Creating Corpus", end='', flush=True)
            with open(DataPath + "RawCorpus.txt", 'w') as outfile:
                for fname in FileNames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
            # Print time elapse
            finishcorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeElapse = (datetime.datetime.strptime(finishcorpus, '%H:%M:%S') -
                          datetime.datetime.strptime(startcorpus, '%H:%M:%S'))
            print(" - Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")
        else:
            print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" +
                  " Corpus already created")

# CreateCorpus(DataPath = '../data/')
