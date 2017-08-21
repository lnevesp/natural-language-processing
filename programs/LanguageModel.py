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

    def __init__(self, File, Method,  Version, SampleTrainRate=0.05, TestModel="no", SampleTestRate=0.01, Seed=123,
                 ForceNGram = "no", NumJobs=1):
        self.color01 = "\033[92m"  # Green

        # Create log data ----------------------------------------------------------------------------------------------
        LogVars = ["ProcessID", "Date", "Start_LanguageModel", "Version", "PC", "Method", "NumJobs", "Time_Total",
                   "Time_DownloadScript", "Time_Download", "Time_WriteCorpus", "Count_CorpusLines", "FileSize_Corpus",
                   "Time_CleanScript", "Time_ReadCorpus", "Time_cleanCorpus", "Count_WordTokens", "Count_TokensLines",
                   "SampleTrainRate", "Seed", "Count_SampleTrainLines", "FileSize_TrainTokens",
                   "Time_LanguageModel", "Time_CreateNGram", "Time_NGramData",
                   "TestModel", "SampleTestRate", "Count_TestLines", "Accuracy", "MeanTime_StupidBackoff",
                   "Stop_LanguageModel"]

        filename = "../data/Log.csv"
        if os.path.isfile(filename) == 1:
            tempLog = pd.read_csv(filename)
            self.infoLog = pd.DataFrame(np.array([[max(tempLog['ProcessID'])]]), columns=['ProcessID'])
        else:
            self.infoLog = pd.DataFrame(np.array(["00001"]), columns=['ProcessID'])

        self.infoLog = self.infoLog.reindex(columns=LogVars)
        self.infoLog['Date'] = of.getDate()
        self.infoLog['Version'] = Version
        self.infoLog['Method'] = Method
        self.infoLog['PC'] = "DELL"
        self.infoLog['Start_LanguageModel'] = of.calcTime()
        self.infoLog['NumJobs'] = NumJobs
        StartScript = of.calcTime()
        self.infoLog['SampleTrainRate'] = SampleTrainRate
        self.infoLog['TestModel'] = TestModel.lower()
        self.infoLog['SampleTestRate'] = SampleTestRate
        self.infoLog['Seed'] = Seed

        # Print Start --------------------------------------------------------------------------------------------------
        of.StartModel(Title=str("Creating Language Model - Version: " + str(Version)),
                      Subtitle=str("Parameters - " + "Method: " + str(Method) +
                                   "; Sample Rate: " + str(SampleTrainRate) + "; # Cores: " + str(NumJobs)),
                      Time=StartScript, K=80)

        # Download Files -----------------------------------------------------------------------------------------------
        DownloadFiles.CreateCorpus(DataPath='../data/', infoLog=self.infoLog)

        # Clean Data ---------------------------------------------------------------------------------------------------
        CleanData.CleanCorpus(Corpus="../data/Corpus.txt", infoLog = self.infoLog)

        # Create Sample ------------------------------------------------------------------------------------------------
        if (os.path.isfile("../data/TrainTokens.txt") != 1 or ForceNGram.lower() == "yes"):
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

            # Create Model ---------------------------------------------------------------------------------------------
            startTime = of.calcTime()
            self.createModel(Method=Method, NumJobs=int(NumJobs))
            self.infoLog['Stop_Ngram'] = of.calcTime()
            self.infoLog['Time_LanguageModel'] = of.deltaTime(start=startTime)
            of.EndScript(start=StartScript, phrase="Language Model Created")

        # TODO: Test Sample --------------------------------------------------------------------------------------------
        flag_test=str(self.infoLog['TestModel']).lower()
        if flag_test == "yes":
            if os.path.isfile("../data/TestTokens.txt") != 1:
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
                self.infoLog['Count_SampleTestLines'] = n  # Sample Size
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
        filename = "./log/Log.csv"
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
    def createModel(self, Method, NumJobs):
        Start_Ngram = of.calcTime()
        self.infoLog['Start_Ngram'] = Start_Ngram

        # Creating Language Model according with the method indicated
        if Method.lower() == "mapreduce":
            of.StartScript(Start_Ngram, "Executing MapReduce Method")
            # Executing shell script.
            # TODO: Read Data from argument instead of hardcoded
            output = "../data/MapReduce"
            mapReduce = "'python Mapper.py' 'python Reducer.py'"
            numJobs = "j" + str(NumJobs)  # Number of Jobs (DataNodes)
            reducers = str(NumJobs)
            shell_command = ["cat '../data/TrainTokens.txt' | ./mc-hdfs.sh " + str(numJobs) + " " +
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
            Start_Time = of.calcTime()
            of.StartScript(Start_Time, "Executing Sequential Method")
            TrainTokens = open('../data/TrainTokens.txt')
            TrainTokens = TrainTokens.readlines()
            Ngram.GenerateNGram(Data=TrainTokens, infoLog=self.infoLog)

        else:
            of.NormalMessage(" is not an available method.")
            self.infoLog['Time_Ngram'] = None


# Simulations
samplerate = 0.05
itr = 2
cores = 8
for i in range(1, (itr + 1)):
    print("\033[41m" + "Running Simulation: " + str(i)+ "/" + str(itr) + " - Part 1/" + str(cores+1) + "\033[0m \n")
    GenerateLanguageModel(File="../data/Tokens.txt", Method="Sequential", Version="Git 0.3", ForceNGram="Yes",
                          SampleTrainRate=samplerate, TestModel="Yes", SampleTestRate=0.01, Seed=17895, NumJobs=1)
    print()
    for j in range(1, (cores + 1)):
        print("\033[41m" + "Running Simulation: " + str(i) + "/" + str(itr) +
              " - Part " + str(j+1) + "/" + str(cores+1) + "\033[0m \n")
        GenerateLanguageModel(File="../data/Tokens.txt", Method="MapReduce", Version="Git 0.3", ForceNGram="Yes",
                              SampleTrainRate=samplerate, TestModel="Yes", SampleTestRate=0.01, Seed=17895, NumJobs=j)
    samplerate = round(samplerate + 0.05, 2)
    gc.collect()