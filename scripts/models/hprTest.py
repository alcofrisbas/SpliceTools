import numpy as np
import matplotlib.pyplot as plt
import os, sys
from scipy.signal import get_window
import utilFunctions as UF
import hprModel as HPR
import stft as STFT

def main(inputFile , window='blackman', M=601, N=1024, t=-100, 
	minSineDur=0.1, nH=100, minf0=350, maxf0=700, f0et=5, harmDevSlope=0.01):
	
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
	  
	# compute spectrogram of residual
	mXr, pXr = STFT.stftAnal(xr, fs, w, N, H)
	  
	# synthesize hpr model
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)

	# output sound file (monophonic with sampling rate of 44100)
	outputFileSines = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel_sines.wav'
	outputFileResidual = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel_residual.wav'
	outputFile = 'output_sounds/' + os.path.basename(inputFile)[:-4] + '_hprModel.wav'

	# write sounds files for harmonics, residual, and the sum
	UF.wavwrite(yh, fs, outputFileSines)
	UF.wavwrite(xr, fs, outputFileResidual)
	UF.wavwrite(y, fs, outputFile)


if __name__ == '__main__':
	main("/Users/backup/Desktop/Python SMS Scripts/ZZZ - Audio tests/PMShoo00.wav")