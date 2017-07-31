import urllib.request
import tarfile
import os.path
import glob
import datetime
import pandas as pd
import Formats as of
import numpy as np

class CreateCorpus:

    def __init__(self, DataPath='../data/', infoLog=pd.DataFrame(np.array([["0001"]]), columns=['ProcessID'])):
        self.infoLog = infoLog  # Log Dictionary
        
        # Print Start Time
        StartScript = of.calcTime()
        of.StartScript(time=StartScript, phrase="Running DownloadFiles.py")

        # Download File
        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:
            self.download(DataPath, File="ANC_Corpora.tar.gz")
        else:
            of.NormalMessage(phrase="Corpora already downloaded")
            self.infoLog['Time_Download'] = None

        # Extract Files
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractfunc(DataPath="../data/", compressFile="ANC_Corpora.tar.gz")
        else:
            of.NormalMessage(phrase="Files already extracted")

        # Create Corpus
        if os.path.isfile(DataPath + "Corpus.txt") != 1:
            self.createCorpus(DataPath)
            self.infoLog['FileSize_Corpus'] = round(os.path.getsize(DataPath + "Corpus.txt") / (1024 * 1024.0), 2)
            # self.infoLog['Time_DownloadScript'] = of.deltaTime(StartScript)
        else:
            of.NormalMessage(phrase="Corpus already created")
            self.infoLog['FileSize_Corpus'] = round(os.path.getsize(DataPath + "Corpus.txt")/(1024*1024.0),2)
            self.infoLog['Time_WriteCorpus'] = None
            self.infoLog['Time_DownloadScript'] = None

        # Print Final Time
        self.infoLog['Time_DownloadScript'] = float(of.deltaTime(StartScript))
        of.EndScript(start=StartScript, phrase="DownloadFiles.py Finished")
        # print(self.infoLog)

    # -----------------------------------------------------------------------------------------------------------------#
    # Check if the files are already downloaded, if not it download it
    def download(self, DataPath, File, URL="https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1"):

        # Print start download time
        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Downloading Corpora")

        # Download ANC Corpora
        urllib.request.urlretrieve(URL, DataPath + File)

        # Print time elapse
        self.infoLog['Time_Download'] = of.deltaTime(start=StartTime)
        of.ElapseEnd(start=StartTime)

    # Extract files function -------------------------------------------------------------------------------------------
    def extractfunc(self, DataPath, compressFile):

        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Extracting Files")

        tar = tarfile.open(DataPath + compressFile, 'r')
        for item in tar:
            tar.extract(item, DataPath)
            if item.name.find(".tar.gz") != -1:
                extractfunc(item.name, "./" + item.name[:item.name.rfind('/')])

        of.ElapseEnd(start=StartTime)

    # Aggregate Files --------------------------------------------------------------------------------------------------
    def createCorpus(self, DataPath):

        StartTime = of.calcTime()
        of.ElapseStart(time=StartTime, phrase="Writing Corpus")

        FileNames = glob.glob('../data/ANC_Corpora/*.txt')

        with open(DataPath + "Corpus.txt", 'w') as outfile:
            for fname in FileNames:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(str(line) + '\n')

        self.infoLog['Time_WriteCorpus'] = of.deltaTime(start=StartTime)
        of.ElapseEnd(start=StartTime)

# CreateCorpus(DataPath='../data/')
