import sys
import re
import fnmatch
import os

def normalizeLines(lines):
    """Normalizes multi-line logger calls, i.e., transform them to
    a single line.  All other lines are unaltered."""

    #outStr = ''
    lineNum = 0
    outLines = []
    wasMultiLineLog = False
    for line in lines:

        # see if the previous line was the first line of
        # a multi-line log call
        if wasMultiLineLog:
            lastLine = outLines.pop()
            outLine = lastLine.rstrip() + ' ' + line.lstrip()
            outLines.append(outLine)
            wasMultiLineLog = False
            continue

        # find a logger call
        logPrefixRE = r'(\s+)Logger(.*)$'
        m = re.match(logPrefixRE, line)

        # if it's not a match, just append the line
        if m is None:
            #tmpFile.write(line)
            outLines.append(line)
            continue

        # if the logging line ends with a semicolon, we just append it too
        if line.endswith(');\n'):
            #tmpFile.write(line)
            outLines.append(line)
            continue

        # at this point we have the first line of a multi-line
        # log call. Append it to the list and set the flag.
        outLines.append(line)
        wasMultiLineLog = True

    return outLines
    
def transformLine(logLine):
    """If the line is an 'old' logger line, transform it appropriately.
    Otherwise, pass it on unaltered."""

    logRegex = r'(\s+)(//)?Logger\.Log\("(.*)",\s+(.*),\s+(.*),\s+"(.*)"(,\s*(.*))?\);'
    m = re.match(logRegex, logLine)

    # if it didn't match, just return the line unaltered
    if m is None:
        return logLine

    # create a mapping of TraceEventType to Common.Logging log method name
    defaultLogLevel = 'Info'
    logLevelDict = {'TraceEventType.Error': 'Error',
                    'TraceEventType.Warning': 'Warn',
                    'TraceEventType.Critical': 'Fatal'}

    # method call name
    logLevel = m.group(5)
    logMethodName = logLevelDict.get(logLevel, defaultLogLevel)
    #print('logMethodName: ' + logMethodName)

    # get old message string
    message = m.group(6)

    # do we have a format string?
    isFormatted = m.group(7) is not None

    leadingWhitespace = m.group(1) or ''
    leadingComment = m.group(2) or ''

    # format the new log call
    newPlainLogStr = '{0}{1}log.{2}("{3}");'
    newFormatLogStr = '{0}{1}log.{2}Format("{3}", {4});'
    if isFormatted:
        args = m.group(8)
        newLogStr = newFormatLogStr.format(leadingWhitespace, leadingComment, logMethodName, message, args)
    else:
        newLogStr = newPlainLogStr.format(leadingWhitespace, leadingComment, logMethodName, message)

    return newLogStr + '\n'

# main script
inDir = sys.argv[1]

files = []
for root, dirnames, filenames in os.walk(inDir):
  for filename in fnmatch.filter(filenames, '*.cs'):
      files.append(os.path.join(root, filename))

# iterate over each csharp file
for file in files:

    print('Preparing to transform file: ' + file)

    myin = open(file, 'r')

    # normalize the 'old' logger lines
    normalizedLines = normalizeLines(myin)

    # close the input file
    myin.close()

    # transform the 'old' logger lines
    transformedLines = [transformLine(line) for line in normalizedLines]

    # create a string from the transformed lines
    outStr = ''.join(line for line in transformedLines)

    # write the transformed lines back out to the input file
    myout = open(file, 'w')
    myout.write(outStr)
    myout.close()

