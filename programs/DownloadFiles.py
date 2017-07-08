import urllib.request
import tarfile
import os.path
import glob
import datetime
from collections import defaultdict
# from Formats import OutputFormats as of
import Formats as of


class CreateCorpus:

    def __init__(self, DataPath = '../data/', infoLog = defaultdict(list)):
        # self.color01 = "\033[92m"  # Values Print Color: Green
        self.infoLog = infoLog  # Log Dictionary
        # self.DataPath = '../data/'
        
        # Print Start Time
        StartScript = of.calcTime()
        of.StartScript(time=StartScript, phrase="Running DownloadFiles.py")

        # Download File
        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:
            self.download(DataPath, File="ANC_Corpora.tar.gz")
        else:
            of.NormalMessage(phrase="Corpora already downloaded")
            self.infoLog['Time_download'] = datetime.timedelta(0)

        # Extract Files
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractfunc(DataPath="../data/", compressFile="ANC_Corpora.tar.gz")
        else:
            of.NormalMessage(phrase="Files already extracted")
            self.infoLog['Time_extractfunc'] = datetime.timedelta(0)

        # Create Corpus
        if os.path.isfile(DataPath + "Corpus.txt") != 1:
            self.createCorpus(DataPath)
        else:
            of.NormalMessage(phrase="Corpus already created")
            self.infoLog['TEWriteCorpus'] = datetime.timedelta(0)

        # Print Final Time
        self.infoLog['TEDownloadScript'] = of.evalElapse(StartScript)
        of.EndScript(start=StartScript, phrase="DownloadFiles.py Finished")

    # Check if the files are already downloaded, if not it download it
    def download(self, DataPath, File, URL="https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1"):

        # Print start download time
        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Downloading Corpora")

        # Download ANC Corpora
        urllib.request.urlretrieve(URL, DataPath + File)

        # Print time elapse
        self.infoLog['Time_download'] = of.evalElapse(start=StartTime)
        of.ElapseEnd(start=StartTime)

    # Extract files function
    def extractfunc(self, DataPath, compressFile):

        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Extracting Files")

        tar = tarfile.open(DataPath + compressFile, 'r')
        for item in tar:
            tar.extract(item, DataPath)
            if item.name.find(".tar.gz") != -1:
                extractfunc(item.name, "./" + item.name[:item.name.rfind('/')])

        self.infoLog['Time_extractfunc'] = of.evalElapse(start=StartTime)
        of.ElapseEnd(start=StartTime)

    # Aggregate Files
    def createCorpus(self, DataPath):

        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Writing Corpus")

        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')

        with open(DataPath + "Corpus.txt", 'w') as outfile:
            for fname in FileNames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

        self.infoLog['Time_createCorpus'] = of.evalElapse(start=StartTime)
        of.ElapseEnd(start=StartTime)



CreateCorpus(DataPath='../data/')
