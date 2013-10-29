#!/usr/bin/python

# 5-line fuzzer below is from Charlie Miller's
# "Babysitting an Army of Monkeys"

from os import listdir
from os.path import isfile, join

mypath = '/users/david/documents/python/pdf/'
file_list = [ mypath+f for f in listdir(mypath) if isfile(join(mypath,f)) ]

apps = ['/Program Files (x86)/Foxit Software/Foxit Reader/Foxit Reader.exe',
'/Program Files (x86)/Adobe/Reader 11.0/Reader/AcroRd32.exe']

fuzz_output = "fuzz.pdf"

FuzzFactor = 2500
num_tests = 100

import math
import random
import string
import subprocess
import time

random.seed(1337)

out = []

for i in range(num_tests):
    file_choice = random.choice(file_list)
    app = random.choice(apps)

    buf = bytearray(open(file_choice, 'rb').read())

    numwrites = random.randrange(math.ceil((float(len(buf)) / FuzzFactor)))+1

    for j in range(numwrites):
        rbyte = random.randrange(256)
        rn = random.randrange(len(buf))
        buf[rn] = "%c"%(rbyte)

    open(fuzz_output, 'wb').write(buf)

    process = subprocess.Popen([app, fuzz_output])

    time.sleep(1)
    crashed = process.poll()
    if not crashed:
        process.terminate()
    else:
        out.append("Attempt #%d crashed!" % (i+1))
        out.append("Application: %s" % app)
        out.append("Return code: %s" % process.returncode)
        out.append("")
        open(fuzz_output + '_' + str(i+1), 'wb').write(buf)
    time.sleep(1)

f = open(mypath[:-4]+'fuzzer.log', 'w')
f.write('\n'.join(out))
f.close()

