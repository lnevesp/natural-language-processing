import urllib.request
import tarfile
import os.path
import glob
import datetime
from collections import defaultdict
from Formats import TimeFormats


class CreateCorpus:

    def __init__(self, DataPath = '../data/'):
        self.color01 = "\033[92m" # Green
        self.color02 = "\033[93m"  # Yellow

        # Start Log dict
        self.infoLog = defaultdict(list)

        # Print Start Time
        self.infoLog['StartDownloadScript'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.StartScript(self, time=self.infoLog['StartDownloadScript'], phrase="Starting DownloadFiles.py")

        self.DataPath = '../data/'
        self.downloadFiles(DataPath)
        self.extractFiles(self.DataPath)
        self.createCorpus(self.DataPath)

        # Print Final Time
        self.infoLog['StopDownloadScript'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEDownloadScript'] = (datetime.datetime.strptime(self.infoLog['StopDownloadScript'], '%H:%M:%S') -
                                            datetime.datetime.strptime(self.infoLog['StartDownloadScript'], '%H:%M:%S'))
        TimeFormats.StopScript(self, StopTime=self.infoLog['StopDownloadScript'],
                               TimeElapse=self.infoLog['TEDownloadScript'], phrase="DownloadFiles.py Finished")


    # Check if the files are already downloaded, if not it download it
    def downloadFiles(self, DataPath):

        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:

            # Print start download time
            self.infoLog['StartDownload'] = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=self.infoLog['StartDownload'], phrase= "Downloading Corpora")

            # Download ANC Corpora
            urllib.request.urlretrieve("https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1",
                                       DataPath + "ANC_Corpora.tar.gz")

            # Print time elapse
            self.infoLog['StopDownload'] = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEDownload'] = (datetime.datetime.strptime(self.infoLog['StopDownload'], '%H:%M:%S') -
                                          datetime.datetime.strptime(self.infoLog['StartDownload'], '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEDownload'])

        else:
            TimeFormats.NormalMessage(self, phrase="Corpora already downloaded")


    # Extract files function
    def extractFunction(self, tar_url, DataPath):

        self.infoLog['StartExtract'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.timeElapse1(self, time=self.infoLog['StartExtract'], phrase="Extracting Files")

        tar = tarfile.open(tar_url, 'r')
        for item in tar:
            tar.extract(item, DataPath )
            if item.name.find(".tar.gz") != -1:
                extractFunction(item.name, "./" + item.name[:item.name.rfind('/')])

        # Print time elapse
        self.infoLog['StopExtract'] = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEExtract'] = (datetime.datetime.strptime(self.infoLog['StopExtract'], '%H:%M:%S') -
                                      datetime.datetime.strptime(self.infoLog['StartExtract'], '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEExtract'])

    # Check if the files are already extracted, if not then do the extraction...
    def extractFiles(self, DataPath):
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractFunction(DataPath + "ANC_Corpora.tar.gz", DataPath = "../data/")
        else:
            TimeFormats.NormalMessage(self, phrase="Files already extracted")


    # Aggregate Files
    def createCorpus(self, DataPath):
        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')
        if os.path.isfile(DataPath + "RawCorpus.txt") != 1:

            self.infoLog['StartWriteCorpus'] = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=self.infoLog['StartWriteCorpus'], phrase="Writing Corpus")

            with open(DataPath + "RawCorpus.txt", 'w') as outfile:
                for fname in FileNames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            # Print time elapse
            self.infoLog['StopWriteCorpus'] = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEWriteCorpus'] = (datetime.datetime.strptime(self.infoLog['StopWriteCorpus'], '%H:%M:%S') -
                                             datetime.datetime.strptime(self.infoLog['StartWriteCorpus'], '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEWriteCorpus'])
        else:
            TimeFormats.NormalMessage(self, phrase="Corpus already created")


# CreateCorpus(DataPath = '../data/')
