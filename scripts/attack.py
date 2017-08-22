import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os, sys
import math
from scipy.signal import get_window
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '../models/'))
import utilFunctions as UF
import hprModel as HPR
import stft as STFT

def cutPoint(inArray, surveyDepth, threshold, stabilityValue):
	"""
	finds a stable point in the given array at the given depth and returns that index
	"""
	surveyLen = inArray.shape[0]
	cutPoint = surveyLen

	for i in range(surveyLen-stabilityValue):
		isCut = False
		values = []
		for j in range(stabilityValue):
			
			error = np.abs(inArray[i, surveyDepth]-inArray[i+j, surveyDepth])
			initVal = inArray[i, surveyDepth]
			compVal = inArray[i+j, surveyDepth]
			values.append(error)
			if error < threshold and initVal != 0 and compVal != 0:
				isCut = True
			else:
				isCut = False
		if isCut:
			cutPoint = i
			break
	return cutPoint
	
def makeSound(hfreq, hmag, hphase, xr, Ns, H, fs, cutPoint, padValue):
	"""
	constructs a sound
	"""
	cutPoint = cutPoint+padValue
	hfreq = np.resize(hfreq, (cutPoint, hfreq.shape[1]))
	hmag = np.resize(hmag, (cutPoint, hmag.shape[1]))
	hphase = np.resize(hphase, (cutPoint, hphase.shape[1]))
	
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)

	return y

def writeSound(y, fs, inputFile):
	'''
	writes a constructed sound to a file
	'''
	outPutAttack = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_attack.wav'
	UF.wavwrite(y, fs, outPutAttack)

def construct(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	"""
	makes arrays of a wav file
	"""
	Ns = 512
	H = 128
	(fs, x) = UF.wavread(inputFile)
	w = get_window(window, M)
	hfreq, hmag, hphase, xr = HPR.hprModelAnal(x, fs, w, N, H, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
	return hfreq, hmag, hphase, xr, fs


def main(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	Ns = 512
	H = 128
	hfreq, hmag, hphase, xr ,fs = construct(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01)
	hfreqAttack = cutPoint(hfreq, 4, 50, 20)
	hmagAttack = cutPoint(hmag, 0, 1, 200)

	print hfreqAttack
	print hmagAttack

	theCut = max(hfreqAttack, hmagAttack)

	yAttack = makeSound(hfreq, hmag, hphase, xr, Ns, H, fs, theCut, 10)

	writeSound(yAttack, fs, inputFile)

	

if __name__ == '__main__':
	main("/Users/backup/Desktop/gits/SpliceTools/sounds/PattyMee_00.wav", nH = 5)