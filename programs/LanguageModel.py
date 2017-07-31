import random
import datetime
import subprocess
import pickle
import Ngram
import DownloadFiles
import CleanData
from Formats import TimeFormats as tf
import pandas as pd
from shutil import rmtree
import os
import numpy as np


class GenerateLanguageModel:

    def __init__(self, ID, File, Method,  Version, Percent):
        self.infoLog = pd.DataFrame(np.array([[ID]]), columns=['ProcessID'])
        self.infoLog['Version'] = Version

        self.infoLog['StartModel'] = tf.calcTimeNow(self)

        # Print Colors:
        self.color01 = "\033[92m" # Green
        tf.StartModel(self, self.infoLog['StartModel'])

        # Download Files
        DownloadFiles.CreateCorpus(DataPath='../data/', infoLog = self.infoLog)

        # Clean Data
        CleanData.CleanCorpus(RawCorpus="../data/RawCorpus.txt", infoLog = self.infoLog)

        # Create Model
        self.createModel(File=File, Method=Method, Percent=Percent)

        self.infoLog['StopModel'] = tf.calcTimeNow(self)
        self.infoLog['TELanguage'] = (tf.formatTime(self, self.infoLog['StopModel']) -
                                      tf.formatTime(self, self.infoLog['StartModel']))

        # TODO: Save log
        print(self.color01 + "\n>>> " + tf.calcTimeNow(self) + "\033[0m" + " Saving Log")
        self.infoLog = pd.DataFrame([self.infoLog])
        filename = "../data/Log.csv"
        self.infoLog.to_csv(filename, index=False, encoding='utf-8')

        print(self.color01 + ">>> " + self.infoLog['StopModel'] + "\033[0m" + " Process Finished")


    def sampling(self, Data, output, N,  percent, seed):

        n = int(round(N*percent, 0))  # Sample Size
        self.infoLog['SampleSize'] = n
        self.infoLog['SampleRate'] = percent
        random.seed(seed)  # Set Seed
        SampleData = [Data[i] for i in sorted(random.sample(range(N), n))]
        with open('../data/' + output, 'wb') as file:
            pickle.dump(SampleData, file, pickle.HIGHEST_PROTOCOL)
        return SampleData

    def createModel(self, File, Method, Percent):
        startReading = tf.calcTimeNow(self)
        print(self.color01 + "\n>>> " + startReading + "\033[0m" +
              " Reading Tokens Data", end='', flush=True)
        with open(File, "rb") as file:  # Unpickling
            Data = pickle.load(file)
        N = len(Data)
        finishReading = tf.calcTimeNow(self)
        TimeElapse = (datetime.datetime.strptime(finishReading, '%H:%M:%S') -
                      datetime.datetime.strptime(startReading, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        # Creating Train Data
        startSampling = tf.calcTimeNow(self)
        print(self.color01 + ">>> " + startSampling + "\033[0m" +
              " Sampling Tokens Data", end='', flush=True)
        self.TrainData = self.sampling(Data=Data, output="SampleTokens.pkl", N=N, percent=Percent, seed=1272)
        finishSampling = tf.calcTimeNow(self)
        TimeElapse = (datetime.datetime.strptime(finishSampling, '%H:%M:%S') -
                      datetime.datetime.strptime(startSampling, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

        # Creating Language Model according with the method indicated
        if Method.lower() == "mapreduce":
            self.startMethod = tf.calcTimeNow(self)
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + " Executing MapReduce Method")
            # Executing shell script.
            # TODO: Read Data from argument instead of hardcoded
            output = "../data/MapReduce"
            mapReduce = "'python Mapper.py' 'python Reducer.py'"
            blocksize = "150m"
            reducers = "8"
            shell_command = ["echo 'SampleTokens.pkl' | ./mc-hdfs.sh " + blocksize + " " +
                             reducers + " " + mapReduce + " " + output]
            if os.path.exists(output):
                rmtree(output)
                subprocess.check_call(shell_command, shell=True)
            else:
                subprocess.check_call(shell_command, shell=True)

        elif Method.lower() == "sequential":
            self.startMethod = tf.calcTimeNow(self)
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + " Executing Sequential Method")
            Ngram.GenerateNGram(Data=self.TrainData, infoLog=self.infoLog)

        else:
            self.startMethod = tf.calcTimeNow(self)
            print(self.color01 + ">>> " + self.startMethod + "\033[0m" + "Error: " +
                  Method + " is not an available method.")

        # Create Test Data.
        startTestData = datetime.datetime.now().time().strftime('%H:%M:%S')
        print(self.color01 + ">>> " + startTestData + "\033[0m" +
              " Creating Test Data", end='', flush=True)
        self.TestData = self.sampling(Data=Data, output="TestData.pkl", N=N, percent=0.01, seed=547)
        finishTestData = tf.calcTimeNow(self)
        TimeElapse = (datetime.datetime.strptime(finishTestData, '%H:%M:%S') -
                      datetime.datetime.strptime(startTestData, '%H:%M:%S'))
        print(self.color01 + " | " + "\033[0m" + "# Sentences: " +
              self.color01 + str(len(self.TestData)) +
              self.color01 + " | " + "\033[0m" + "Time Elapse: " +
              self.color01 + str(TimeElapse) + "\033[0m")


GenerateLanguageModel(ID="0001", File="../data/Tokens.txt", Method="mapreduce", Version="Git 0.1", Percent=0.30)
