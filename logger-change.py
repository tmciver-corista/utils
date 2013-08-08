import sys
import re
import pprint

#inFile = r'C:\Users\Tim McIver\Documents\workspace\ExportService\MiraxReader\src\MiraxSlideReader.cs'
#outFile = r'C:\Users\Tim McIver\Documents\workspace\ExportService\MiraxReader\src\MiraxSlideReader-post.cs'
inFile = sys.argv[1]

defaultLogLevel = 'Info'
logLevelDict = {'TraceEventType.Error': 'Error',
                'TraceEventType.Warning': 'Warn',
                'TraceEventType.Critical': 'Fatal'}

newPlainLogStr = '{0}log.{1}("{2}");'
newFormatLogStr = '{0}log.{1}Format("{2}", {3});'

logPrefixRE = r'(\s+)Logger(.*)$'
logRE = r'(\s+)Logger\.Log\("(.*)",\s+(.*),\s+(.*),\s+"(.*)"(,\s*(.*))?\);'

myin = open(inFile, 'r')
#out = open(outFile, 'w')

# first, fix logging lines that are broken across two lines
#tmpFile = open('tmp.cs', 'w')
outStr = ''
lineNum = 0
for line in myin:

    # find a logger call
    m = re.match(logPrefixRE, line)

    # if it's not a match, just write the line
    if m is None:
        #tmpFile.write(line)
        outStr = outStr + line
        continue

    #print(outStr)

    # if the logging line ends with a semicolon, we just write it too
    if line.endswith(');\n'):
        #tmpFile.write(line)
        outStr = outStr + line
        continue

    # read the next line and remove the whitespace at the front
    nextLine = myin.readline()
    #lineNum = lineNum + 1

    # write the concantenation of these two lines to the file
    outStr = outStr + line.rstrip() + ' ' + nextLine.lstrip()
    #tmpFile.write(line.rstrip() + ' ' + nextLine.lstrip())

# some cleanup
#tmpFile.close()
myin.close()

# now, operate on tmpFile and do the transformation
myout = open(inFile, 'w')
#tmpFile = open('tmp.cs', 'r')
#tmpFile2 = open('tmp2.cs', 'w')
#print(outStr)
lines = outStr.split('\n')
print('Number of lines: ' + str(len(lines)))
#sys.exit(0)
for line in lines:

    # find a logger call
    m = re.match(logRE, line)

    # if it's not a match, just write the line
    if m is None:
        myout.write(line + '\n')
        continue

##    pprint.pprint(m.groups())
##    continue

    # method call name
    logLevel = m.group(4)
    logMethodName = logLevelDict.get(logLevel, defaultLogLevel)
    #print('logMethodName: ' + logMethodName)

    # get old message string
    message = m.group(5)

    # do we have a format string?
    isFormatted = m.group(6) is not None

    leadingWhitespace = m.group(1)

    # format the new log call
    if isFormatted:
        args = m.group(7)
        newLogStr = newFormatLogStr.format(leadingWhitespace, logMethodName, message, args)
    else:
        newLogStr = newPlainLogStr.format(leadingWhitespace, logMethodName, message)

    #print('Will replace old log line:\n' + line + 'with this one:\n' + newLogStr + '\n')
    myout.write(newLogStr + '\n')


myout.close()
#tmpFile2.close()

##while line = myin.readline()
##
##with open(inFile, 'r') as myin:
##    data = myin.read()
##    m = re.findall(logRE, data)
##    #m = re.search(logRE, data)
##    pprint.pprint(m)
##    print(len(m))
##    if m is not None:
##        print(m.groups())

