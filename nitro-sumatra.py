# The original code is obtained here:
# http://forums.udacity.com/questions/100231307/my-two-fuzzers-for-pdf-readers-foxit-reader-and-adobe-acroreader-and-for-potplayer-mp3-files#cs258


import math
import random
import string
import subprocess
import time
import os
import datetime
import codecs

apps = [
    "C:/Program Files (x86)/Nitro/Reader 3/NitroPDFReader.exe",
    "E:/Software/SumatraPDF-3.0/SumatraPDF.exe"
]

fuzz_input_dir = "J:/Data/pdfFuzzerTargets2"

fuzz_output = "J:/Data/pdfFuzzerTemp/fuzz.pdf"

fuzz_output_folder = "J:/Data/pdfFuzzerTemp/"

fuzz_log = codecs.open("J:/Data/pdfFuzzerResult/log_" + time.strftime("%Y%m%d%H%M%S.txt"), "w", "utf-8")


#So the fuzz factor controls the number of bytes to be changed
#The lower the factor, the more bytes that will be modified.
FuzzFactor = 250

num_tests = 20000

numberOfCrashes=0

file_list = []

for root, subFolders, files in os.walk(fuzz_input_dir):
    for file in files:
        file_list.append(os.path.join(root,file))

fuzz_log.write("Starts at " + str(datetime.datetime.now()) + '\n')



for i in range(num_tests):
    
    file_choice = random.choice(file_list)
    
    #app = random.choice(apps)

    app = apps[1]

    buf = bytearray(open(file_choice, 'rb').read())

    numwrites = random.randrange(math.ceil((float(len(buf)) / FuzzFactor))) + 1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = rbyte

    open(fuzz_output, 'wb').write(buf)

    process = subprocess.Popen([app, fuzz_output])
    time.sleep(1)

    fuzz_log.write("File " + file_choice + ": ")

    crashed = process.poll()
    if crashed:

        numberOfCrashes += 1

        appName = app.split("/")[len(app.split("/"))-1]
        print(str(numberOfCrashes) + " crashed application: " + appName)
        fuzz_log.write(str(numberOfCrashes) + " crashed application: " + appName + "\n")

        # save this crash input for later forensics
        open(fuzz_output_folder + "crash_input" + str(numberOfCrashes) + ".pdf", "wb").write(buf)
    else:
        process.terminate()
        fuzz_log.write("\n")
    time.sleep(1)

print ("The number of crashes is %s of %s"%(numberOfCrashes, num_tests))
fuzz_log.write("The number of crashes is %s of %s"%(numberOfCrashes, num_tests) + "\n")
fuzz_log.write("Ends at " + str(datetime.datetime.now()))
fuzz_log.close()
