__module_name__ = "inline-sctime"
__module_version__ = "0.1"
__module_description__ = "Detects distances like '40kls', '1 ly', '2,000 ls' and injects a !sctime estimate into the message"

import hexchat
import re

distanceRegex = r'(?P<distance>(?P<value>\d+(\.\d+|,\d+)?)\s*(?P<unit>ls|kls|mls|ly))'

unitFactors = {
    'ls': 1,
    'kls': 1000,
    'mls': 1000000,
    'ly': 31557600
}

#parses distance and returns a number in light seconds
def parseDistance(distRegexMatch):
    distNum = float(distRegexMatch.group('value').replace(',', '.'))
    distUnits = distRegexMatch.group('unit')
    return convertToLS(distNum, distUnits)

#converts supported units into light seconds
def convertToLS(distNum, distUnits):
    distUnits = distUnits.lower()
    return distNum * unitFactors.get(distUnits, 0)

#runs !sctime calculations and returns total seconds to travel
def calcTotalSeconds(lightSeconds):
    if lightSeconds < 100000:
        return int(pow(lightSeconds, 0.3292) * 8.9034)

    elif lightSeconds < 1907087:
        val1 = -8 * pow(10, -23) * pow(lightSeconds, 4)
        val2 = 4 * pow(10, -16) * pow(lightSeconds, 3) - 8 * pow(10, -10) * pow(lightSeconds, 2)
        val3 = 0.0014 * lightSeconds + 264.79
        return int(val1+val2+val3)

    else:
        return int((lightSeconds - 5265389.609) / 2001 + 3412)

#converts total seconds into human readable format
def createTimeString(totalSeconds):
    hours = totalSeconds // 3600
    remainderSec = totalSeconds % 3600
    minutes = remainderSec // 60
    seconds = totalSeconds % 60

    if(hours > 0):
        formattedTime = '({0}h{1}m{2}s)'.format(hours, minutes, seconds)
    elif(minutes > 0):
        formattedTime = '({0}m{1}s)'.format(minutes, seconds)
    else:
        formattedTime = '({0}s)'.format(seconds)

    return f'\035{formattedTime}\035'


def injectSCTime(word, word_eol, event):
    if word[1].startswith('\u200c'):
        return hexchat.EAT_NONE

    distRegexMatch = re.search(distanceRegex, word[1], re.IGNORECASE)
    if distRegexMatch:
        distance = parseDistance(distRegexMatch)
        totalTime = calcTotalSeconds(distance)
        timeString = createTimeString(totalTime)

        distanceWithTime = f'{distRegexMatch.group("distance")} {timeString}'
        updatedMessage = re.sub(distanceRegex, distanceWithTime, word[1], flags=re.IGNORECASE)

        word[1] = f'\u200c{updatedMessage}'
        hexchat.emit_print(event, *word)
        return hexchat.EAT_ALL

    return hexchat.EAT_NONE

hexchat.hook_print("Channel Message", injectSCTime, "Channel Message")
hexchat.hook_print("Your Message", injectSCTime, "Your Message")
