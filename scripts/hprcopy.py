# function to call the main analysis/synthesis functions in software/models/hprModel.py

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

def freqCutPoint(hfreq, surveyDepth, threshold, stabilityValue):
	surveyLen = hfreq.shape[0]
	cutPoint = surveyLen

	for i in range(surveyLen-stabilityValue):
		
		isCut = False
		values = []
		for j in range(stabilityValue):
			
			error = np.abs(hfreq[i, surveyDepth]-hfreq[i+j, surveyDepth])
			initVal = hfreq[i, surveyDepth]
			compVal = hfreq[i+j, surveyDepth]
			values.append(error)
			if error < threshold and initVal != 0 and compVal != 0:
				isCut = True
			else:
				isCut = False
		if isCut:
			cutPoint = i
			
			break

	hfreqCut = np.resize(hfreq, (cutPoint, hfreq.shape[1]))
	fillLength =  surveyLen-cutPoint
	hfreqFill = np.full((fillLength, hfreq.shape[1]),0.001)

	hfreqAttack = np.concatenate((hfreqCut, hfreqFill))
	return hfreqAttack



def main(inputFile, window='blackman', M=601, N=1024, t=-100, 
	minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	"""
	Perform analysis/synthesis using the harmonic plus residual model
	inputFile: input sound file (monophonic with sampling rate of 44100)
	window: analysis window type (rectangular, hanning, hamming, blackman, blackmanharris)	
	M: analysis window size; N: fft size (power of two, bigger or equal than M)
	t: magnitude threshold of spectral peaks; minSineDur: minimum duration of sinusoidal tracks
	nH: maximum number of harmonics; minf0: minimum fundamental frequency in sound
	maxf0: maximum fundamental frequency in sound; f0et: maximum error accepted in f0 detection algorithm                                                                                            
	harmDevSlope: allowed deviation of harmonic tracks, higher harmonics have higher allowed deviation
	"""

	# size of fft used in synthesis
	Ns = 512

	# hop size (has to be 1/4 of Ns)
	H = 128

	# read input sound
	(fs, x) = UF.wavread(inputFile)

	# compute analysis window
	w = get_window(window, M)

	# find harmonics and residual
	hfreq, hmag, hphase, xr = HPR.hprModelAnal(x, fs, w, N, H, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
	#print hfreq.shape[1]
	#print hmag.shape

	
	hfreqAttack = freqCutPoint(hfreq, 4, 50, 20)
	hmagAttack = freqCutPoint(hmag, 0, 1, 200)

	# compute spectrogram of residual
	mXr, pXr = STFT.stftAnal(xr, fs, w, N, H)
	  
	# synthesize hpr model
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)
	

	# output sound file (monophonic with sampling rate of 44100)
	outputFileSines = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel_sines.wav'
	outputFileResidual = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel_residual.wav'
	outputFile = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel.wav'
	output_FileAttack = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_attack.wav'

	# write sounds files for harmonics, residual, and the sum
	#UF.wavwrite(yh, fs, outputFileSines)
	#UF.wavwrite(xr, fs, outputFileResidual)
	#UF.wavwrite(y, fs, outputFile)
	#UF.wavwrite()

	# create figure to plot
	plt.figure(figsize=(12, 9))

	# frequency range to plot
	maxplotfreq = 2500.0
	colors = iter(cm.rainbow(np.linspace(0, 1, 10)))
	plt.subplot(4,1,1)
	harms = hfreqAttack*np.less(hfreqAttack,maxplotfreq)
	harms[harms==0] = np.nan
	numFrames = int(harms[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs) 
	plt.plot(frmTime, harms, color = 'k', ms=3, alpha=1)
	plt.xlabel('time(s)')
	plt.ylabel('frequency(Hz)')
	plt.autoscale(tight=True)
	plt.title('attack')

	# plot the magnitude spectrogram of residual
	plt.subplot(4,1,2)
	maxplotbin = int(N*maxplotfreq/fs)
	numFrames = int(mXr[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs)                       
	binFreq = np.arange(maxplotbin+1)*float(fs)/N                         
	#plt.pcolormesh(frmTime, binFreq, np.transpose(mXr[:,:maxplotbin+1]))
	#plt.autoscale(tight=True)

	# plot harmonic frequencies on residual spectrogram
	if (hfreq.shape[1] > 0):#if there is more than 0 columns
		#shape is arranged as (row, column)
		harms = hfreq*np.less(hfreq,maxplotfreq)
		harms[harms==0] = np.nan
		numFrames = int(harms[:,0].size)
		frmTime = H*np.arange(numFrames)/float(fs) 
		plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
		plt.xlabel('time(s)')
		plt.ylabel('frequency(Hz)')
		plt.autoscale(tight=True)
		plt.title('harmonics, total')

	# plot the output sound
	plt.subplot(4,1,3)
	amps = hmag*np.less(hmag,maxplotfreq)
	amps[amps==0] = np.nan
	numFrames = int(amps[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs) 
	plt.plot(frmTime, amps, color='k', ms=3, alpha=1)
	plt.ylabel('amplitude')
	plt.xlabel('time (sec)')
	plt.title('amplitude')

	plt.subplot(4,1,4)
	amps = hmagAttack*np.less(hmagAttack,maxplotfreq)
	amps[amps==0] = np.nan
	numFrames = int(amps[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs) 
	plt.plot(frmTime, amps, color='k', ms=3, alpha=1)
	plt.ylabel('amplitude')
	plt.xlabel('time (sec)')
	plt.title('amplitude')

	plt.tight_layout()
	plt.show()

if __name__ == '__main__':
	#main("/Users/backup/Desktop/Python SMS Scripts/ZZZ - Audio tests/PMShoo00.wav")
	main("/Users/backup/Desktop/Python SMS Scripts/ZZZ - Audio tests/PMShoo00.wav", nH = 5)
