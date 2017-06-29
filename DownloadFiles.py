import urllib.request
import tarfile
import os.path
import glob
import datetime
from collections import defaultdict
from Formats import TimeFormats


class CreateCorpus:

    def __init__(self, DataPath = '../data/', infoLog = defaultdict(list)):
        self.color01 = "\033[92m"  # Values Print Color: Green
        self.infoLog = infoLog  # Log Dictionary

        # Print Start Time
        StartDownloadScript = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.StartScript(self, time=StartDownloadScript, phrase="Starting DownloadFiles.py")

        self.DataPath = '../data/'
        self.downloadFiles(DataPath)
        self.extractFiles(self.DataPath)
        self.createCorpus(self.DataPath)

        # Print Final Time
        StopDownloadScript = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEDownloadScript'] = (datetime.datetime.strptime(StopDownloadScript, '%H:%M:%S') -
                                            datetime.datetime.strptime(StartDownloadScript, '%H:%M:%S'))
        TimeFormats.StopScript(self, TimeElapse=self.infoLog['TEDownloadScript'], phrase="DownloadFiles.py Finished")

    # Check if the files are already downloaded, if not it download it
    def downloadFiles(self, DataPath):

        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:

            # Print start download time
            StartDownload = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=StartDownload, phrase="Downloading Corpora")

            # Download ANC Corpora
            urllib.request.urlretrieve("https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1",
                                       DataPath + "ANC_Corpora.tar.gz")

            # Print time elapse
            StopDownload = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEDownload'] = (datetime.datetime.strptime(StopDownload, '%H:%M:%S') -
                                          datetime.datetime.strptime(StartDownload, '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEDownload'])

        else:
            TimeFormats.NormalMessage(self, phrase="Corpora already downloaded")
            self.infoLog['TEDownload'] = datetime.timedelta(0)


    # Extract files function
    def extractFunction(self, tar_url, DataPath):

        StartExtract = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeFormats.timeElapse1(self, time=StartExtract, phrase="Extracting Files")

        tar = tarfile.open(tar_url, 'r')
        for item in tar:
            tar.extract(item, DataPath )
            if item.name.find(".tar.gz") != -1:
                extractFunction(item.name, "./" + item.name[:item.name.rfind('/')])

        # Print time elapse
        StopExtract = datetime.datetime.now().time().strftime('%H:%M:%S')
        self.infoLog['TEExtract'] = (datetime.datetime.strptime(StopExtract, '%H:%M:%S') -
                                     datetime.datetime.strptime(StartExtract, '%H:%M:%S'))
        TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEExtract'])

    # Check if the files are already extracted, if not then do the extraction...
    def extractFiles(self, DataPath):
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractFunction(DataPath + "ANC_Corpora.tar.gz", DataPath = "../data/")
        else:
            TimeFormats.NormalMessage(self, phrase="Files already extracted")
            self.infoLog['TEExtract'] = datetime.timedelta(0)

    # Aggregate Files
    def createCorpus(self, DataPath):
        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')
        if os.path.isfile(DataPath + "RawCorpus.txt") != 1:

            StartWriteCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
            TimeFormats.timeElapse1(self, time=StartWriteCorpus, phrase="Writing Corpus")

            with open(DataPath + "RawCorpus.txt", 'w') as outfile:
                for fname in FileNames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)

            # Print time elapse
            StopWriteCorpus = datetime.datetime.now().time().strftime('%H:%M:%S')
            self.infoLog['TEWriteCorpus'] = (datetime.datetime.strptime(StopWriteCorpus, '%H:%M:%S') -
                                             datetime.datetime.strptime(StartWriteCorpus, '%H:%M:%S'))
            TimeFormats.timeElapse2(self, TimeElapse=self.infoLog['TEWriteCorpus'])
        else:
            TimeFormats.NormalMessage(self, phrase="Corpus already created")
        self.infoLog['TEWriteCorpus'] = datetime.timedelta(0)


# CreateCorpus(DataPath = '../data/')
