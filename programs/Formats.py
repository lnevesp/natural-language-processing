import datetime
import time

def calcTime():
    return datetime.datetime.now().time().strftime('%H:%M:%S')

def getDate():
    return time.strftime("%Y/%m/%d")
# Format time
def formatTime(time):
    return datetime.datetime.strptime(time, '%H:%M:%S')

# Evaluate Time Elapse
def evalElapse(start):
    TimeElapse = formatTime(calcTime()) - formatTime(start)
    return TimeElapse

def deltaTime(start):
    delta = formatTime(calcTime()) - formatTime(start)
    return round(delta.seconds + delta.microseconds / 1E6,2)

# Print Format for beginning of a script
def StartScript(time, phrase):
    color01 = "\033[92m"
    print(color01 + "\n >>> " + "\033[0m" +
          phrase + " - " + color01 + time + "\033[0m")

# Print Format for end of a script
def EndScript(start, phrase):
    color01 = "\033[92m"
    print(color01 + " >>> " "\033[0m" +
          phrase + color01 + " | " + "\033[0m" +
          "Time Elapse: " + color01 + str(evalElapse(start)) + "\033[0m")

# Continuous Message with Time Elapse: Beginning of Message
def ElapseStart(time, phrase):
    color01 = "\033[92m"
    print(color01 + " >>>  " + time + "\033[0m" +
          " " + phrase, end='', flush=True)

# Continuous Message with Time Elapse: End of Message
def ElapseEnd(start):
    color01 = "\033[92m"
    print(color01 + " | " + "\033[0m" + "Time Elapse: " +
          color01 + str(evalElapse(start)) + "\033[0m")

# Normal Message
def NormalMessage(phrase):
    color01 = "\033[92m"
    print(color01 + " >>>  " + calcTime() + "\033[0m" + " " + phrase)

# Beginning of Procedure Improve this
def StartModel(Title, Subtitle, Time, K=60):
    color01 = "\033[92m"
    length = len(str(Time) + "  " + Title)
    empty = K-length
    completeTitle = ' '*int((empty/2)-1)

    length = len(Subtitle)
    empty = K-length
    completeSubTitle = ' '*int((empty/2)-1)

    print(color01 + ' +' + '-'*K + '+')
    print(color01 + ' |' + '='*K + '|')
    print(color01 + ' |  ' + "\033[0m" + completeTitle + color01 + str(Time) + "\033[0m" + "  " + Title + completeTitle + color01 + '|')
    print(color01 + ' |' + '-'*K + '|')
    print(color01 + ' |  ' + "\033[0m" + completeSubTitle + Subtitle + completeSubTitle + color01 + '|')
    print(color01 + ' |' + '='*K + '|')
    print(color01 + ' +' + '-'*K + '+')
