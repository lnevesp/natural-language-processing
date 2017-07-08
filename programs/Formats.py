import datetime


    # Returns the present time and format it
def calcTime():
    return datetime.datetime.now().time().strftime('%H:%M:%S')

# Format time
def formatTime(time):
    return datetime.datetime.strptime(time, '%H:%M:%S')

# Evaluate Time Elapse
def evalElapse(start):
    TimeElapse = formatTime(calcTime()) - formatTime(start)
    return TimeElapse

# Print Format for beginning of a script
def StartScript(time, phrase):
    color01 = "\033[92m"
    print(color01 + "\n>>> " + "\033[0m" +
          phrase + " - " + color01 + time + "\033[0m")

# Print Format for end of a script
def EndScript(start, phrase):
    color01 = "\033[92m"
    print(color01 + ">>> " "\033[0m" +
          phrase + color01 + " | " + "\033[0m" +
          "Time Elapse: " + color01 + str(evalElapse(start)) + "\033[0m")

# Continuous Message with Time Elapse: Beginning of Message
def ElapseStart(time, phrase):
    color01 = "\033[92m"
    print(color01 + ">>>  " + time + "\033[0m" +
          " " + phrase, end='', flush=True)

# Continuous Message with Time Elapse: End of Message
def ElapseEnd(start):
    color01 = "\033[92m"
    print(color01 + " | " + "\033[0m" + "Time Elapse: " +
          color01 + str(evalElapse(start)) + "\033[0m")

# Normal Message
def NormalMessage(phrase):
    color01 = "\033[92m"
    print(color01 + ">>>  " + calcTime() + "\033[0m" + " " + phrase)

# Beginning of Procedure
def StartModel(phrase, time, k=60):
    color01 = "\033[92m"
    length = len(phrase)
    empty = k-length
    completeRow = ' '*int((empty/2)-9)
    title = (completeRow + phrase + ' ')
    print(color01 + ' +' + '-'*k + '+')
    print(color01 + ' |' + '_'*k + '|')
    print(color01 + ' |  ' + "\033[0m" + title + color01 + str(time) + completeRow + '|')
    print(color01 + ' |' + '_'*k + '|')
    print(color01 + ' +' + '-'*k + '+')
