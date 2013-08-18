import os
import subprocess
import time
import datetime

# globals
exePath = r'C:\Users\Tim McIver\Documents\workspace\ExportService\bin\Debug\Corista.ExportService.Console.exe'
perfFileDirPath = '//enterprise/banks/export-service-perf'
outputTopLevelDirPath = r'C:\Corista\Processed'
inputFileBasePath = '//enterprise/banks/slides'

# create a list of run data
# the data is a list of tuples; the tuples contain the reader name followed by
# the path to the input slide file.
runData = [('Mirax', inputFileBasePath + '/Mirax/DHMC-001.mrxs'),
           ('AperioLegacy', inputFileBasePath + '/Aperio/Aperio Legacy/Liver2.svs'),
           ('OpenSlide', inputFileBasePath + '/Leica/S13-22808;2;A;1100005416591;1_2013-05-10 20_42_28.scn'),
           ('BioImagene', inputFileBasePath + '/BioImagene/DH_2_10_200904031056.jp2')]

for data in runData:
    # get the reader name
    readerName = data[0]

    # get the input file path
    inputFilePath = '"' + data[1] + '"'

    #print(inputFilePath)
    #continue

    # get the input file name
    [pathpart, inputFileName] = os.path.split(inputFilePath)

    # get the filename without extension
    basename = os.path.splitext(inputFileName)[0]

    # create a new output dir with an appropriate subdir name
    outputDirPath2 = outputTopLevelDirPath + '\\' + basename

    # generate a date string
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')

    # costruct the stdout output file name
    stdoutFilePath = perfFileDirPath + '/' + readerName + '_' + basename + '_' + st + '.out'
    #print(outputname)
    #return

    # run the export service console app
    args = exePath + ' -i ' + inputFilePath + ' -o ' + outputDirPath2 + ' -t ' + readerName

    # open the output file
    out = open(stdoutFilePath, 'w')

    # debug
    #print(args)
    #continue
    
    proc = subprocess.Popen(args, stdout=out)

    # wait for it
    proc.wait()

    # close the output file
    out.close()
