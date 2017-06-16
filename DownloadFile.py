import urllib.request
import tarfile
import os.path
import glob
from time import gmtime, strftime, time

class CreateCorpus:

    def __init__(self, DataPath = '../data/'):
        print("Iniciated at: " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        self.DataPath = '../data/'
        self.downloadFiles(DataPath)
        self.extractFiles(self.DataPath)
        self.createCorpus(self.DataPath)


    # Check if the files are already downloaded, if not it download it
    def downloadFiles(self, DataPath):
        if os.path.isfile(DataPath + "ANC_Corpora.tar.gz") != 1:
            print("Downloading Corpora...")
            urllib.request.urlretrieve("https://www.dropbox.com/s/hbmn0rbkujnxqrt/ANC_Corpora.tar.gz?dl=1", DataPath + "ANC_Corpora.tar.gz")
        else:
            print("Corpora already downloaded")

    # Extract files function
    def extractFunction(self, tar_url, DataPath):
        print ("Extracting: " + tar_url)
        tar = tarfile.open(tar_url, 'r')
        for item in tar:
            tar.extract(item, DataPath )
            if item.name.find(".tar.gz") != -1:
                extractFunction(item.name, "./" + item.name[:item.name.rfind('/')])

    # Check if the files are already extracted, if not then do the extraction...
    def extractFiles(self, DataPath):
        if os.path.isdir(DataPath + "ANC_Corpora/") != 1:
            self.extractFunction(DataPath + "ANC_Corpora.tar.gz", DataPath = "../data/")
        else:
            print("Files already extracted")

    # Aggregate Files
    def createCorpus(self, DataPath):
        # Read *.txt File names
        FileNames = glob.glob('../data/ANC_Corpora/*.txt')
        if os.path.isfile(DataPath + "RawCorpus.txt") != 1:
            print("Creating Corpus...")
            with open(DataPath + "RawCorpus.txt", 'w') as outfile:
                for fname in FileNames:
                    with open(fname) as infile:
                        for line in infile:
                            outfile.write(line)
        else:
            print("Corpus already created")

CreateCorpus(DataPath = '../data/')
