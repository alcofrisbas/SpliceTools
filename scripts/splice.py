from attack import *
import numpy as np

def freqAvg(hfreq, n):
	length = hfreq.shape[0]
	sum_arr = np.sum(hfreq, axis=0)
	return sum_arr[n]/length

def lastFreq(hfreq, n, hfreqAttack):
	hfreq = np.resize(hfreq, (hfreqAttack, hfreq.shape[1]))
	return hfreq[-1, n]

def pitchRatio(attack, tone):
	return attack/tone
"""
use testTrim to trim the tone file
"""


#input attack:
inputFile = "/Users/backup/Desktop/Python SMS Scripts/ZZZ - Audio tests/PMShoo00.wav"
hfreq, hmag, hphase, xr, fs = construct(inputFile)
Ns = 512
H = 128

print xr.shape

tone = freqAvg(hfreq, 0)

hfreqAttack = cutPoint(hfreq, 4, 50, 20)

attack = lastFreq(hfreq, 0, hfreqAttack)

print pitchRatio(attack, tone)

hmagAttack = cutPoint(hmag, 0, 1, 200)

theCut = max(hfreqAttack, hmagAttack)

yAttack = makeSound(hfreq, hmag, hphase, xr, Ns, H, fs, theCut, 10)

writeSound(yAttack, fs, inputFile)

def main(attackFile, toneFile, ):
	Ns = 512
	H = 128
	hfreqA, hmagA, hphaseA, xr, fs = construct(attackFile)
	hfreqT, hmagT, hphaseT, xr, fs = construct(toneFile)

