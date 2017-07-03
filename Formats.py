import datetime


class TimeFormats:

    def calcTimeNow(self):
        return datetime.datetime.now().time().strftime('%H:%M:%S')

    def formatTime(self, time):
        return datetime.datetime.strptime(time, '%H:%M:%S')

    def StartScript(self, time, phrase):
        print(self.color01 + "\n>>> " + "\033[0m" +
              phrase + " - " + self.color01 + time + "\033[0m")

    def StopScript(self, TimeElapse, phrase):
        print(self.color01 + ">>> " "\033[0m" +
              phrase + self.color01 + " | " + "\033[0m" +
              "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    def timeElapse1(self, time, phrase):
        print(self.color01 + ">>>  " + time + "\033[0m" +
              " " + phrase, end='', flush=True)

    def timeElapse2(self, TimeElapse):
        print(self.color01 + " | " + "\033[0m" + "Time Elapse: " + self.color01 + str(TimeElapse) + "\033[0m")

    def NormalMessage(self, phrase):
        print(self.color01 + ">>>  " + datetime.datetime.now().time().strftime('%H:%M:%S') + "\033[0m" +
              " " + phrase)

    def StartModel(self, time):
        print(self.color01 + '  ##################################################')
        print(self.color01 + '  ##                                              ##')
        print(self.color01 + '  ##  ' + "\033[0m" + 'Starting Language Model Generation ' + self.color01 + str(time) + ' ##')
        print(self.color01 + '  ##                                              ##')
        print(self.color01 + '  ##################################################')
