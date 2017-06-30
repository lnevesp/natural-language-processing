import random
import datetime
from collections import defaultdict
import subprocess
import pickle
import Ngram
import DownloadFiles
import CleanData
from Formats import TimeFormats as tf


class GenerateLanguageModel:

    def __init__(self, File, Method , Percent):
        self.startModel = datetime.datetime.now().time().strftime('%H:%M:%S')

        self.infoLog = defaultdict(list)
        # Print Colors:
        self.color01 = "\033[92m" # Green
        self.color02 = "\033[93m" # Yellow
        print(self.color01 + ">>> " + self.startModel + "\033[0m" + " Starting Language Model Generation")

        # Download Files
        DownloadFiles.CreateCorpus(DataPath = '../data/', infoLog = self.infoLog)

        # Clean Data
        CleanData.CleanCorpus(RawCorpus="../data/RawCorpus.txt", infoLog = self.infoLog)

        # Create Model
        self.createModel(File=File, Method=Method, Percent=Percent)
        self.FinishModel = datetime.datetime.now().time().strftime('%H:%M:%S')

        print(self.color01 + "\n>>> " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" + "Saving Log")
        # TODO: Save log


        TimeElapse = (datetime.datetime.strptime(self.FinishModel, '%H:%M:%S') -
                      datetime.datetime.strptime(self.startModel, '%H:%M:%S'))




        print(self.color01 + "\n>>> " + self.FinishModel + "\033[0m" + " Process Finished" +
              self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse))

        print(self.infoLog)

    def sampling(self, Data, output, N,  percent):

        n = int(round(N*percent, 0))  # Sample Size
        self.infoLog['SampleSize'] = n
        self.infoLog['SampleRate'] = percent
        random.seed(123)  # Set Seed
        SampleData = [Data[i] for i in sorted(random.sample(range(N), n))]
        with open('../data/' + output, 'wb') as file:
            pickle.dump(SampleData, file, pickle.HIGHEST_PROTOCOL)
        return SampleData

    def createModel(self, File, Method, Percent):
        startReading = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + "\n>>> " + startReading + "\033[0m" +
              " Reading Tokens Data", end='', flush=True)
        with open(File, "rb") as file:  # Unpickling
            Data = pickle.load(file)
        N = len(Data)
        finishReading = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishReading, '%H:%M:%S') -
                      datetime.datetime.strptime(startReading, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        # Creating Train Data
        startSampling = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>> " + startSampling + "\033[0m" +
              " Sampling Tokens Data", end='', flush=True)
        self.TrainData = self.sampling(Data=Data, output="SampleTokens.pickle", N=N, percent=Percent)
        finishSampling = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishSampling, '%H:%M:%S') -
                      datetime.datetime.strptime(startSampling, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        # Creating Language Model according with the method indicated
        if Method.lower() == "mapreduce":
            self.startMethod = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + " Executing MapReduce Method")
            # Executing shell script.
            subprocess.check_call(["echo 'SampleTokens.pickle' | ../multicore-hdfs/mc-hdfs.sh 5m 8 'python Mapper.py' 'python Reducer.py' ../data/MapReduceOutput_00001"], shell=True)
        elif Method.lower() == "sequential":
            self.startMethod = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + " Executing Sequential Method")
            Ngram.GenerateNGram(Data=self.TrainData, infoLog=self.infoLog)
        else:
            self.startMethod = datetime.datetime.now().time().strftime('%H:%M:%S')
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + "Error: " + Method + " is not an available method.")

        # Create Test Data.
        startTestData = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>> " + startTestData + "\033[0m" +
              " Creating Test Data", end='', flush=True)
        self.TestData = self.sampling(Data=Data, output="TestData.pickle", N=N, percent=0.00001)
        finishTestData = datetime.datetime.now().time().strftime('%H:%M:%S')
        TimeElapse = (datetime.datetime.strptime(finishTestData, '%H:%M:%S') -
                      datetime.datetime.strptime(startTestData, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "# Sentences: " +
              self.color01 + str(len(self.TestData)) +
              self.color01 + " | " + "\033[0m" + "Time Elapse: " +
              self.color01 + str(TimeElapse) + "\033[0m")


GenerateLanguageModel(File="../data/Tokens.pickle", Method="sequential", Percent=0.10)

# import profile
# profile.run('GenerateLanguageModel(File="../data/Tokens.pickle", Method="Sequential", Percent=0.01)')
