
__module_name__ = "inline-sctime"
__module_version__ = "0.1"
__module_description__ = "Detects distances like '40kls', '1 ly', '2,000 ls' and injects a !sctime estimate into the message"

import hexchat
import re
from datetime import timedelta

print("Inline-SCTime Script Loaded")

distanceRegex = '((\d+|,|\.)+)\s?(kls|mls|ls|ly)'

#bulk of the work, takes value like "50kls" and returns an sctime estimate like "(1h23m4s)"
def parseDistance(distRegexMatch):
    distNum = int(str(distRegexMatch[1]).replace(',','').replace('.',''))
    distUnits = distRegexMatch[distRegexMatch.lastindex]
    distLs = convertToLS(distNum, distUnits)
    totalSeconds = calcTotalSeconds(distLs)
    return createTimeString(totalSeconds)
    
#converts one of the supported units (Mls, kls, ly, ls) to light seconds (ls)
def convertToLS(distNum, distUnits):

    distUnits = distUnits.lower()
    if(distUnits == 'mls'):
        return distNum * 1000000
    elif(distUnits == 'kls'):
        return distNum * 1000
    elif(distUnits == 'ly'):
        return distNum * 31557600
    elif(distUnits == 'ls'):
        return distNum
    else:
        #regex should not allow this to happen
        return 0

#ripped straight from SwiftSqueak (mecha3), calculates total seconds to travel given light seconds
def calcTotalSeconds(lightSeconds):
    if(lightSeconds < 100000):
        return int(pow(lightSeconds,0.3292) * 8.9034)
    elif(lightSeconds < 1907087):
        val1 = -8 * pow(10,-23) * pow(lightSeconds,4)
        val2 = 4 * pow(10,-16) * pow(lightSeconds,3) - 8 * pow(10,-10) * pow(lightSeconds,2)
        val3 = 0.0014 * lightSeconds + 264.79
        return int(val1+val2+val3)
    else:
        return int((lightSeconds-5265389.609)/2001+3412)

#takes total seconds and converts it to a human readable format like "(7h2m23s)"
def createTimeString(totalSeconds):
    hours = totalSeconds // 3600
    remainderSec = totalSeconds % 3600
    minutes = remainderSec // 60
    seconds = totalSeconds % 60
    
    if(hours > 0):
        toReturn = '({0}h{1}m{2}s)'.format(hours, minutes, seconds)
    elif(minutes > 0):
        toReturn = '({0}m{1}s)'.format(minutes, seconds)
    else:
        toReturn = '({0}s)'.format(seconds)

    return '\035' + toReturn + '\035'

#hook function
def injectSCTime(word, word_eol, event):

    if str(word[1]).startswith('\u200c'):
        return hexchat.EAT_NONE

    distRegexMatch = re.search(distanceRegex, word[1], re.IGNORECASE)
    if (distRegexMatch):
        sctime = parseDistance(distRegexMatch)
        word[1] = '\u200c' + re.sub(distanceRegex, distRegexMatch[0] + sctime, word[1], re.IGNORECASE)
        hexchat.emit_print(event, *word)
        return hexchat.EAT_ALL
     
    return hexchat.EAT_NONE
    
 

hexchat.hook_print("Channel Message", injectSCTime, "Channel Message")
hexchat.hook_print("Your Message", injectSCTime, "Your Message")

#for outside testing
'''testMessage = '#3 bc+ 200kls prep-'
testMessage2 = 'foobar'

distRegexMatch = re.search(distanceRegex, testMessage)
if (distRegexMatch):
    sctime = parseDistance(distRegexMatch)
    testMessage = re.sub(distanceRegex, distRegexMatch[0] + sctime, testMessage)
    
print(testMessage)'''