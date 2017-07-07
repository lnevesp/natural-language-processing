import urllib.request
import tarfile
import os.path
import glob
import datetime
from collections import defaultdict
from Formats import TimeFormats as tf


class CreateCorpus:

    def __init__(self, DataPath = '../data/', infoLog = defaultdict(list)):
        self.color01 = "\033[92m"  # Values Print Color: Green
        self.infoLog = infoLog  # Log Dictionary

        # Print Start Time
        StartDownloadScript = tf.calcTimeNow(self)
        tf.StartScript(self, time=StartDownloadScript, phrase="Starting DownloadFiles.py")

        self.DataPath = '../data/'
        self.downloadFiles(DataPath)
        self.extractFiles(self.DataPath)
        self.createCorpus(self.DataPath)

        # Print Final Time
        self.infoLog['TEDownloadScript'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                            tf.formatTime(self, StartDownloadScript))
        tf.StopScript(self, TimeElapse=self.infoLog['TEDownloadScript'], phrase="DownloadFiles.py Finished")

    # Check if the files are already downloaded, if not it download it
    def downloadFiles(self, DataPath):

        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:

            # Print start download time
            StartDownload = tf.calcTimeNow(self)
            tf.timeElapse1(self, time=StartDownload, phrase="Downloading Corpora")

            # Download ANC Corpora
            urllib.request.urlretrieve("https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1",
                                       DataPath + "ANC_Corpora.tar.gz")

            # Print time elapse
            # StopDownload = tf.calcTimeNow(self)
            self.infoLog['TEDownload'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                          tf.formatTime(self, StartDownload))
            tf.timeElapse2(self, TimeElapse=self.infoLog['TEDownload'])

        else:
            tf.NormalMessage(self, phrase="Corpora already downloaded")
            self.infoLog['TEDownload'] = datetime.timedelta(0)


    # Extract files function
    def extractFunction(self, compressFile, DataPath):

        StartExtract = tf.calcTimeNow(self)
        tf.timeElapse1(self, time=StartExtract, phrase="Extracting Files")

        tar = tarfile.open(compressFile, 'r')
        for item in tar:
            tar.extract(item, DataPath )
            if item.name.find(".tar.gz") != -1:
                tf(item.name, "./" + item.name[:item.name.rfind('/')])

        # Print time elapse
        # StopExtract = tf.calcTimeNow(self)
        self.infoLog['TEExtract'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                     tf.formatTime(self, StartExtract))
        tf.timeElapse2(self, TimeElapse=self.infoLog['TEExtract'])

    # Check if the files are already extracted, if not then do the extraction...
    def extractFiles(self, DataPath):
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractFunction(DataPath + "ANC_Corpora.tar.gz", DataPath = "../data/")
        else:
            tf.NormalMessage(self, phrase="Files already extracted")
            self.infoLog['TEExtract'] = datetime.timedelta(0)

    # Aggregate Files
    def createCorpus(self, DataPath):
        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')
        if os.path.isfile(DataPath + "RawCorpus.txt") != 1:

            StartWriteCorpus = tf.calcTimeNow(self)
            tf.timeElapse1(self, time=StartWriteCorpus, phrase="Writing Corpus")

            with open(DataPath + "RawCorpus.txt", 'w') as outfile:
                for fname in FileNames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            self.infoLog['TEWriteCorpus'] = (tf.formatTime(self, tf.calcTimeNow(self)) -
                                             tf.formatTime(self, StartWriteCorpus))
            tf.timeElapse2(self, TimeElapse=self.infoLog['TEWriteCorpus'])
        else:
            tf.NormalMessage(self, phrase="Corpus already created")
        self.infoLog['TEWriteCorpus'] = datetime.timedelta(0)


# CreateCorpus(DataPath='../data/')
