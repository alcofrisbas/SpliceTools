import numpy as np
import soundfile as sf
import time
import math

from scipy.signal import get_window

import hprModel as HPR

INT16_FAC = (2**15)-1
INT32_FAC = (2**31)-1
INT64_FAC = (2**63)-1
norm_fact = {'int16':INT16_FAC, 'int32':INT32_FAC, 'int64':INT64_FAC,'float32':1.0,'float64':1.0}



def zeroPad(x, fs, ms):
	arr = np.zeros(ms*fs/1000)							#construct silence array of correct millisecond length									#
	padded = np.concatenate((arr, x), axis=0)			#add the two arrays together
	#print soundLength(padded, fs)-soundLength(x, fs)	#check for correctness
	padded = np.float32(padded)/norm_fact[padded.dtype.name]
	return padded, fs

def soundLength(x, fs):
	return (float(x.shape[0])/fs)*1000					#return length of sound in ms

def soundToArray(soundFile):
	(x, fs) = sf.read(soundFile)						#get array and sample rate of soundFile
	x = np.float32(x)/norm_fact[x.dtype.name]			#turn array into numpy array of the correct bit depth
	return x, fs

def numSamples(x):
	return x.shape[0]									#returns number of samples in a sound
def numFrames(hArray):
	return hArray.shape[0]								#returns number of frames in a sound
def samplesPerFrame(x, hArray):
	return float(numSamples(x))/numFrames(hArray)
def framesPerSecond(fs, spf):
	"""
	fs: sample rate(samples per second)
	spf: samples per frame
	"""
	return float(fs)/spf 								#returns frames per second
def framesPerSecond2(length, numFrames):
	length = length/1000.0
	return numFrames/length 

def infoAt(hPhase, f):
	return hPhase[f, 0]									#returns information at that point
def pitchRatio(consF, vowelF):
	if consF == 0 or vowelF == 0:
		return 1
	return consF/vowelF 								#returns the pitch ratio


def retune(fs, y, stepRatio):							#retunes the given sound using linear interpolation
    
    lastI = len(y)/float(stepRatio)
    #print lastI
    newsound = []
    for i in range(int(lastI+1)):
        newsound.append(0)
    for i in range(int(lastI)):
        iTemp = stepRatio*i
        intItemp = int(iTemp)
        xfrac = iTemp - intItemp
        newsound[i] += y[intItemp] + xfrac * (y[intItemp+1]-y[intItemp])
    arr = np.asarray(newsound)
    return np.float32(arr)/norm_fact[arr.dtype.name]

							#returns frames per second using another method

def fourierResidual(x, fs, window='blackman', M=601, N=1024, t=-100, minSineDur=0.1, nH=20, minf0=200, maxf0=300, f0et=5, harmDevSlope=0.01):
	Ns = 512											#
	H = 128												#hop size

	w = get_window(window, M)							#get analysis window
	hfreq, hmag, hphase, xr = HPR.hprModelAnal(x, fs, w, N, H, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
	return hfreq, hmag, hphase, xr						#returns 2D arrays and 1D array of residual sound

def stablePoint(inHarmonicArray, surveyDepth, threshold, stabilityValue, pad):
	"""
	inHarmonicArray: hfreq or hmag
	surveyDepth: which harmonic to test for stability
	threshold: error threshold
	stabilityValue: number of frames to test for stability
	"""
	surveyLen = inHarmonicArray.shape[0]				#duration of sound for for loop
	cutPoint = surveyLen 								#sets default cutPoint just in case none is found

	for i in range(surveyLen-stabilityValue):
		isCut = False									#indicator that a cut point has been found
		values = []										#empty list of error values
		for j in range(stabilityValue):					#compares array values with values j ahead and logs error values
			error = np.abs(inHarmonicArray[i, surveyDepth]-inHarmonicArray[i+j, surveyDepth])
			initVal = inHarmonicArray[i, surveyDepth]
			compVal = inHarmonicArray[i+j, surveyDepth]
			values.append(error)
			if error < threshold and initVal != 0 and compVal != 0:
				isCut = True
			else:
				isCut = False
		if isCut:
			cutPoint = i
			break
	return cutPoint+pad

def adjustPhase(H, consFS, conshfreq, conshphase, cfLF, swF, vowelhphase):
	HopTime = float(H)/consFS
	freqPeriod = 1/conshfreq[swF, 1]

	for i in range(conshphase.shape[1]):
		for j in range(1, cfLF):
			before = conshphase[swF-cfLF+j+1, i]
			conshphase[swF-cfLF+j+1, i] = (conshphase[swF-cfLF+j, i] + (2*math.pi)*HopTime*conshfreq[swF-cfLF+j, i]) % (2*math.pi)
		phaseCorr = (vowelhphase[swF, i] - conshphase[swF, i])% (2*math.pi)
		phaseCorrIncremental = -1*phaseCorr/cfLF
		for j in range(1, int(cfLF+1)):
			conshphase[swF-cfLF+j, i] = (conshphase[swF-cfLF+j, i]+phaseCorrIncremental)%(2*math.pi)

def crossFadePitch(conshfreq, vowelhfreq, swF, cfLF):
	start = swF-cfLF
	for i in range(1, conshfreq.shape[1]):
		if conshfreq[swF - cfLF, i] == 0:
			continue
		PitchDiff = conshfreq[swF, i]-conshfreq[swF - cfLF, i]
		for j in range(1, int(cfLF)):
			conshfreq[start+j, i] = conshfreq[start+j, i]+((j/cfLF)*PitchDiff)

def adjustMagnitude(conshmag, vowelhmag, stable, vowelPadF):
	for i in range(conshmag.shape[1]):

		ratio = conshmag[stable, i]/vowelhmag[stable+vowelPadF, i]
		for j in conshmag[i]:
			conshmag[j,i] = conshmag[j,i]*ratio

def simpleXFade(consX, vowelX, consFS, swF, cfL, conshfreq):
	swSample = swF*samplesPerFrame(consX, conshfreq)
	addAmount = vowelX.shape[0]-consX.shape[0]
	if addAmount > 0:
		consX = np.concatenate((consX, np.zeros(addAmount)))
	else:
		consX = np.resize(consX, vowelX.shape[0])
	
	for i in range(0, consX.shape[0]):
		if i < swSample-cfL:
			vowelX[i] = 0
		elif i < swSample:
			realNumber = swSample-i
			scaleAmount = realNumber/cfL

			consX[i] = consX[i]*scaleAmount
			vowelX[i] = vowelX[i]*(1-scaleAmount)
		else:
			consX[i] = 0

	#sf.write("output_sounds/simpleXFadeCons.wav", consX, consFS)
	#sf.write("output_sounds/simpleXFadeVowel.wav", vowelX, consFS)

	x = np.add(consX, vowelX)
	#sf.write("output_sounds/simpleXFade.wav", x, consFS, subtype="PCM_24")
	return x

def makeSound(hfreq, hmag, hphase, xr, Ns, H, fs):
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)
	return y, yh

def writeSound(fileName, x, fs):
	sf.write(fileName, x, fs, subtype="PCM_24")

def splice(consFile, vowelFile, cfL, pad, vowelPadMs, f0min, f0max, Ns=512, H=128):
	consX, consFS = soundToArray(consFile)				#read both files to arrays
	vowelX, vowelFS = soundToArray(vowelFile)			#and capture their sample rate

	if consFS != vowelFS:								#make sure that sample rates match
		raise ValueError("Please use samples with matching Sample Rates")

	vowelX, vowelFS = zeroPad(vowelX, vowelFS, 700)		#rewrite the vowel file with
														#a pad of VOWELPADMS ms

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, minf0 = f0min, maxf0 = f0max)
	vowelhfreq, vowelhmag, vowelhphase, vowelxr = fourierResidual(vowelX, vowelFS, minf0 = f0min, maxf0 = f0max)
														#using SMS Tools, construct arrays
														#of the components of each sound
	vowelPadF = (vowelPadMs/1000.0)*framesPerSecond2(soundLength(vowelX, vowelFS), numFrames(vowelhfreq))
														#the vowel pad in Frames(vs samples or ms)
	cfLF = cfL/samplesPerFrame(consX, conshfreq)		#cfL in Frames(vs samples)
	
	freqStable = stablePoint(conshfreq, 0, 100, 20, pad)#find the stable point of the frequency
	magStable =  stablePoint(conshmag, 0, 40, 10, pad)	#find the stable point of the ampliitude

	stable = max(freqStable, magStable)					#take the maximum for stable point
	if stable == conshfreq.shape[0]+pad:				#However, the highest never detects one
		stable = min(freqStable, magStable)				#use the lower value

	adjustMagnitude(conshmag, vowelhmag, stable, vowelPadF)#adjusts the magnitudes of each harmonic
														#to match with the vowel's harmonics

	consFreqF0 = infoAt(conshfreq, stable)				#find the f0 frequency of the consonant at the stable point
	vowelFreqF0 = infoAt(vowelhfreq, 1.0*framesPerSecond(vowelFS, samplesPerFrame(vowelX, vowelhfreq)))
														#find the f0 frequency of the vowel at the stable point
	pR = pitchRatio(consFreqF0, vowelFreqF0)			#find the pitch ration between the frequencies
	initialNumFrames = numFrames(conshfreq)				#number of frames in the consonant sound

	if pR != 1:											#stretch or shrink the consonant as necessary
		consX = retune(consFS, consX, 1.0/pR)			#to match its pitch to the vowel's

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, minf0 = f0min, maxf0 = f0max)
														#re-harmonic-ize the consonant
	afterRetuneNumFrames = numFrames(conshfreq)			#the duration in Frames of the consonant after the stretch

	stable = int(stable*(float(afterRetuneNumFrames)/initialNumFrames))#calculate where the stable frame is after the retune
	consFreqF0 = infoAt(conshfreq, stable)				#find the new frequency at the new stable point

	padAmount = 1000 - (stable*samplesPerFrame(consX, conshfreq)/consFS)*1000
														#set pad amount to line up the consonant \/ \/ \/ \/
	consX, consFS = zeroPad(consX, consFS, padAmount)	#add enough samples to put the cut point at 1 second into consonant
	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, minf0 = f0min, maxf0 = f0max)
														#create harmonic arrays from the padded consonant
	stable += padAmount/1000*framesPerSecond2(soundLength(consX, consFS), numFrames(conshfreq))
														#add the correct amount of frames to the stable cutpoint value
	crossFadePitch(conshfreq, vowelhfreq, int(stable), cfLF)
														#crossfade-tune the pitches of the harmonics to make the transition smoother
	adjustPhase(H, consFS, conshfreq, conshphase, int(cfLF), int(stable), vowelhphase)
														#adjust the phases of the harmonics to match with the vowel
	consX, consXH = makeSound(conshfreq, conshmag, conshphase, consxr, Ns, H, consFS)
														#write each harmonic (using SMS tools) to a wavy array
	consFreqF0 = infoAt(conshfreq, 1.0*framesPerSecond(consFS, samplesPerFrame(consX, conshfreq)))
														#f0 of consonant
	newX = simpleXFade(consX, vowelX, consFS, stable, cfL, conshfreq)
														#xfade the two using simple cross fade
	writeSound("output_sounds/xFade.wav", newX, consFS)


def main():
	splice("../Morgan_44.1/Mod/Mod_20.wav", "../Morgan_44.1/Ah Main/Ah Main_20.wav", 1000, 25, 700, 200, 300, Ns=512, H=128)
if __name__ == '__main__':
	main()