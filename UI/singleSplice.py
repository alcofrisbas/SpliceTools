from scripts.soundOps import *
import os, sys
from os.path import isfile, join
import numpy as np
consFile = "/Users/backup/Desktop/Python\ SMS\ Scripts/ZZZ\ -\ Audio\ tests/Patty_Test_sample/Patty\ Ah.wav".replace("\\", "")
vowelFile = "/Users/backup/Desktop/Python\ SMS\ Scripts/ZZZ\ -\ Audio\ tests/Patty_Test_sample/Patty\ Ee.wav".replace("\\", "")
outFile = "testSingle.wav".replace("\\", "")

def average_harms(a):
    return [(sum([a[j][i] for j in range(_in, _out)])/float(len(a))) for i in range(len(a[0]))]


def diff(a, b):
    return np.subtract(a,b)


def modify_harms(a, aug):
    l = []
    for j in range(len(a)):
        print(j)
        m = []
        for i in range(len(a[0])):
            m.append(a[j][i]-aug[i])
        l.append(m)
    return l

f0min = 940
f0max = 1040
Ns = 512
H = 128

_in = 500
_out = 900

consX, consFS = soundToArray(consFile)
vowelX, vowelFS = soundToArray(vowelFile)

conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, f0min, f0max, Ns,H)
vowelhfreq, vowelhmag, vowelhphase, vowelxr = fourierResidual(vowelX, vowelFS, f0min, f0max,Ns, H)

print(len(conshfreq))
print(len(vowelhfreq))

avs_conshmag = average_harms(conshmag)
avs_vowelhmag = average_harms(vowelhmag)
diff_hmag = diff(avs_conshmag, avs_vowelhmag)
new_conshmag = modify_harms(conshmag, diff_hmag)
print(len(new_conshmag), len(conshmag))
print(avs_conshmag)
print(avs_vowelhmag)
print(diff_hmag)

y, yh = makeSound(conshfreq, new_conshmag, conshphase, consxr, Ns, H, 44100)
writeSound(outFile, y, 44100)
