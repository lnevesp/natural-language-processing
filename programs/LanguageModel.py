import random
import subprocess
import Ngram
import DownloadFiles
import CleanData
import JoinReduce
import Formats as of
import pandas as pd
from shutil import rmtree
import os
import numpy as np
import gc


class GenerateLanguageModel:

    def __init__(self, ID, File, Method,  Version, SampleTrainRate=0.05, TestModel="no", SampleTestRate=0.01, Seed=123):
        self.color01 = "\033[92m"  # Green

        # Create log data ----------------------------------------------------------------------------------------------
        LogVars = ["ProcessID", "Date", "Start_LanguageModel", "Time_Total", "Version", "PC", "Method", "Seed",
                   "SampleTrainRate", "Count_SampleTrainLines", "TestModel", "SampleTestRate", "Time_LanguageModel",
                   "Time_DownloadScript", "Time_Download", "Time_WriteCorpus", "FileSize_Corpus", "Count_CorpusLines",
                   "Time_CleanScript", "Time_ReadCorpus", "FileSize_TrainTokens", "Count_WordTokens", "Time_cleanCorpus", "Count_TokensLines",
                   "Start_Ngram", "Time_CreateNGram", "Time_NGramData", "Stop_Ngram"]

        self.infoLog = pd.DataFrame(np.array([[ID]]), columns=['ProcessID'])
        self.infoLog = self.infoLog.reindex(columns = LogVars)
        self.infoLog['Date'] = of.getDate()
        self.infoLog['Version'] = Version
        self.infoLog['Method'] = Method
        self.infoLog['PC'] = "ASUS"
        self.infoLog['Start_LanguageModel'] = of.calcTime()
        StartScript = of.calcTime()
        self.infoLog['SampleTrainRate'] = SampleTrainRate
        self.infoLog['TestModel'] = TestModel.lower()
        self.infoLog['SampleTestRate'] = SampleTestRate
        self.infoLog['Seed'] = Seed

        # Print Start --------------------------------------------------------------------------------------------------
        of.StartModel(phrase=str("Creating Language Model - Version: " + str(Version) + "; Method: " + str(Method) +
                                 "; Sample Rate: " + str(SampleTrainRate)),
                      time=StartScript, k=140)

        # Download Files -----------------------------------------------------------------------------------------------
        DownloadFiles.CreateCorpus(DataPath='../data/', infoLog=self.infoLog)

        # Clean Data ---------------------------------------------------------------------------------------------------
        CleanData.CleanCorpus(Corpus="../data/Corpus.txt", infoLog = self.infoLog)

        # Create Sample ------------------------------------------------------------------------------------------------
        # if os.path.isfile("../data/TrainTokens.txt") != 1:
        startTime = of.calcTime()
        of.ElapseStart(startTime, "Reading Tokens Data")
        with open(File, "r") as file:
            Data = file.readlines()
        N = len(Data)
        n = int(round(N*SampleTrainRate, 0))
        self.infoLog['Count_TokensLines'] = N
        self.infoLog['Count_SampleTrainLines'] = n  # Sample Size
        of.ElapseEnd(startTime)

        # Creating Train Data
        startTime = of.calcTime()
        of.ElapseStart(startTime, "Sampling Tokens Data")
        self.TrainData = self.sampling(Data=Data, output="TrainTokens.txt", N=N, Size=n, seed=Seed, Type="train")
        FileSize_TrainTokens = round(os.path.getsize("../data/TrainTokens.txt") / (1024 * 1024.0), 2)
        self.infoLog['FileSize_TrainTokens'] = FileSize_TrainTokens
        of.ElapseEnd(startTime)

        # Create Model -------------------------------------------------------------------------------------------------
        self.createModel(Method=Method)

        # Print Finish Log ---------------------------------------------------------------------------------------------
        self.infoLog['Stop_Ngram'] = of.calcTime()
        self.infoLog['Time_LanguageModel'] = of.deltaTime(start=StartScript)
        of.EndScript(start=StartScript, phrase="Language Model Created")

        # TODO: Test Sample --------------------------------------------------------------------------------------------
        flag_test=str(self.infoLog['TestModel']).lower()
        if flag_test == "yes":
            if os.path.isfile("../data/TrainTokens.txt") != 1:
                startTime = of.calcTime()
                of.ElapseStart(startTime, "Reading Tokens Data")
                try:
                    Data
                except NameError:
                    N = len(Data)
                else:
                    with open(File, "r") as file:
                        Data = file.readlines()
                        N = len(Data)
                self.infoLog['Count_TokensLines'] = N
                n = int(round(N * SampleTestRate, 0))
                self.infoLog['Count_SampleTrainLines'] = n # Sample Size
                of.ElapseEnd(startTime)

                # Creating Train Data
                startTime = of.calcTime()
                of.ElapseStart(startTime, "Creating Sample Test")
                TestData = self.sampling(Data=Data, output="TestTokens.txt", N=N,
                                         Size=self.infoLog['Count_SampleTrainLines'], seed=214, Type="Test")

                with open("../data/TestTokens.txt", 'w') as outfile:
                    # Select Last Words
                    for line in TestData:
                        length = len(line)
                        if length > 4:
                            line = line[-5:]
                            Sentence = line[:-1]
                            Answer = line[-1:]
                        elif length > 1:
                            Sentence = line[:-1]
                            Answer = line[-1:]
                        if Answer:
                            line = str('{},{}'.format(' '.join(Sentence), Answer))
                            outfile.write(line)

                self.infoLog['FileSize_TestTokens'] = round(os.path.getsize("../data/TestTokens.txt") /
                                                             (1024 * 1024.0), 2)
                of.ElapseEnd(startTime)

        # Save Log -----------------------------------------------------------------------------------------------------
        print(self.color01 + "\n>>> " + of.calcTime() + "\033[0m" + " Saving Log")
        self.infoLog['Time_Total'] = float(of.deltaTime(StartScript))
        # self.infoLog = pd.DataFrame([self.infoLog])
        filename = "../data/Log.csv"
        if os.path.isfile(filename) == 1:
            tempLog = pd.read_csv(filename)
            LogFile = tempLog.append(self.infoLog)
            LogFile.to_csv(filename, index=False, encoding='utf-8')
        else:
            self.infoLog.to_csv(filename, index=False, encoding='utf-8')
        # print(self.infoLog)
        print(self.color01 + ">>> " + of.calcTime() + "\033[0m" + " Process Finished")

    # Sampling Function ------------------------------------------------------------------------------------------------
    def sampling(self, Data, output=None, N=None,  Size=None, seed=None, Type="train"):

        random.seed(int(seed))  # Set Seed
        SampleData = [Data[i] for i in random.sample(range(N), int(Size))]
        if Type.lower() == "train":
            with open('../data/' + output, 'w') as outfile:
                for line in SampleData:
                    outfile.write(str(line))

        return SampleData

    # Create Model Function --------------------------------------------------------------------------------------------
    def createModel(self, Method):
        Start_Ngram = of.calcTime()
        self.infoLog['Start_Ngram'] = Start_Ngram

        # Creating Language Model according with the method indicated
        if Method.lower() == "mapreduce":
            of.StartScript(Start_Ngram, "Executing MapReduce Method")
            # Executing shell script.
            # TODO: Read Data from argument instead of hardcoded
            output = "../data/MapReduce"
            mapReduce = "'python Mapper.py' 'python Reducer.py'"
            blocksize = "5m"
            reducers = "8"
            shell_command = ["cat '../data/TrainTokens.txt' | ./mc-hdfs.sh " + str(blocksize) + " " +
                             reducers + " " + mapReduce + " " + output]
            if os.path.exists(output):
                rmtree(output)
                Start_Time = of.calcTime()
                subprocess.check_call(shell_command, shell=True)
                self.infoLog['Time_CreateNGram'] = float(of.deltaTime(Start_Time))
                Start_Time = of.calcTime()
                JoinReduce.JoinReduceFiles(DataPath='../data/', infoLog=self.infoLog)
                self.infoLog['Time_NGramData'] = float(of.deltaTime(Start_Time))
            else:
                Start_Time = of.calcTime()
                subprocess.check_call(shell_command, shell=True)
                self.infoLog['Time_CreateNGram'] = float(of.deltaTime(Start_Time))
                Start_Time = of.calcTime()
                JoinReduce.JoinReduceFiles(DataPath='../data/', infoLog=self.infoLog)
                self.infoLog['Time_NGramData'] = float(of.deltaTime(Start_Time))

        elif Method.lower() == "sequential":
            of.StartScript(self.infoLog['Start_Ngram'], "Executing Sequential Method")
            TrainTokens = open('../data/TrainTokens.txt')
            TrainTokens = TrainTokens.readlines()
            Ngram.GenerateNGram(Data=TrainTokens, infoLog=self.infoLog)

        else:
            of.NormalMessage(" is not an available method.")
            self.infoLog['Time_Ngram'] = None

for i in range(1, 10):
    GenerateLanguageModel(ID=str(i), File="../data/Tokens.txt", Method="sequential", Version="Git 0.1",
                          SampleTrainRate=round(i/100, 2), TestModel="No", SampleTestRate=0.01, Seed=17895)
    gc.collect()