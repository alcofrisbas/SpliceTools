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
import soundfile as sf

INT16_FAC = (2**15)-1
INT32_FAC = (2**31)-1
INT64_FAC = (2**63)-1
norm_fact = {'int16':INT16_FAC, 'int32':INT32_FAC, 'int64':INT64_FAC,'float32':1.0,'float64':1.0}


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
	
def makeSound(hfreq, hmag, hphase, xr, Ns, H, fs, cutPoint, 	):
	"""
	constructs a sound
	"""
	cutPoint = cutPoint+padValue
	hfreq = np.resize(hfreq, (cutPoint, hfreq.shape[1]))
	hmag = np.resize(hmag, (cutPoint, hmag.shape[1]))
	hphase = np.resize(hphase, (cutPoint, hphase.shape[1]))
	
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)

	return y

def makeY(hfreq, hmag, hphase, xr, Ns, H, fs):
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)
	return y

def writeSound(y, fs, name):
	'''
	writes a constructed sound to a file if the sound is 16bit,
	the program uses the utilFunctions module to write the sound,
	otherwise, it uses the python library sound and writes at
	24bits.
	'''
	outPutAttack = name
	if fs == 44100:
		UF.wavwrite(y, fs, outPutAttack)
	else:
		sf.write(outPutAttack, y, fs, subtype="PCM_24")

def construct(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	"""
	makes arrays of a wav file
	"""
	Ns = 512
	H = 128
	(x, fs) = sf.read(inputFile)
	#print "x.dtype", x.dtype
	#print "fs", fs
	x = np.float32(x)/norm_fact[x.dtype.name]
	#(fs, x) = UF.wavread(inputFile)
	#if fs != 44100:
	#	(x, fs) = sf.read(inputFile)
	#	print "x.dtype", x.dtype
	#	print "fs", fs
	#	x = np.float32(x)/norm_fact[x.dtype.name]

	#print "x.dtype", x.dtype
	w = get_window(window, M)
	hfreq, hmag, hphase, xr = HPR.hprModelAnal(x, fs, w, N, H, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
	
	return hfreq, hmag, hphase, xr, fs, x


def main(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	Ns = 512
	H = 128
	inputFile = inputFile.replace("\\", "")
	hfreq, hmag, hphase, xr ,fs = construct(inputFile, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01)
	hfreqAttack = cutPoint(hfreq, 4, 100, 20)
	hmagAttack = cutPoint(hmag, 0, 1, 200)
	print fs
	print "total:", hfreq.shape[0]
	print "frequency:", hfreqAttack
	print "amplitude:", hmagAttack


	theCut = max(hfreqAttack, hmagAttack)
	if theCut == hfreq.shape[0]:
		theCut = min(hfreqAttack, hmagAttack)

	yAttack = makeSound(hfreq, hmag, hphase, xr, Ns, H, fs, theCut, 100)

	writeSound(yAttack, fs, inputFile[:-4]+"asdf.wav")

	

if __name__ == '__main__':
	main("/Users/backup/Documents/Samples/Morgan\ Realivox/Morgan\ Samples/Ah\ False/AhFalse_26.wav", nH = 5)