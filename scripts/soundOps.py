import numpy as np
import soundfile as sf
import time

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
	return hPhase[f, 0]
def pitchRatio(consF, vowelF):
	if consF == 0 or vowelF == 0:
		return 1
	return consF/vowelF


def retune(fs, y, stepRatio):
    
    lastI = len(y)/float(stepRatio)
    print lastI
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

def f0phaseShiftAmount(consPhase, vowelPhase, consFS, consFreqF0):
	samplesPerWave = float(consFS)/consFreqF0			#aka period, don't know why i didnt call it that

def crossFadePitch(conshfreq, vowelhfreq, swF, cfL):
	pass#for 

def adjustMagnitude(conshmag, vowelhmag, stable, vowelPadF):
	print conshmag.shape
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
	print int(swSample-cfL), consX.shape[0]
	
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

	sf.write("output_sounds/simpleXFadeCons.wav", consX, consFS)
	sf.write("output_sounds/simpleXFadeVowel.wav", vowelX, consFS)

	x = np.add(consX, vowelX)
	sf.write("output_sounds/simpleXFade.wav", x, consFS, subtype="PCM_24")
	#sf.write("output_sounds/simpleXFade.wav", )
def makeSound(hfreq, hmag, hphase, xr, Ns, H, fs):
	y, yh = HPR.hprModelSynth(hfreq, hmag, hphase, xr, Ns, H, fs)
	return y, yh

def main():
	startTime = time.time()
	consFile = "../Morgan_44.1/Mod/Mod_18.wav"
	vowelFile = "../Morgan_44.1/Ah Main/Ah Main_20.wav"

	consX, consFS = soundToArray(consFile)
	#print consX, consFS
	vowelX, vowelFS = soundToArray(vowelFile)
	#print vowelX, vowelFS
	if consFS != vowelFS:
		raise ValueError("Please use samples with matching Sample Rates")
	vowelPadMs = 700
	vowelX, vowelFS = zeroPad(vowelX, vowelFS, 700)		#add .7 seconds to vowel

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS)
														#construct harmonic arrays from consonant sound
	vowelhfreq, vowelhmag, vowelhphase, vowelxr = fourierResidual(vowelX, vowelFS)
														#construct harmonic arrays from padded vowel sound
	vowelPadF = (vowelPadMs/1000.0)*framesPerSecond2(soundLength(vowelX, vowelFS), numFrames(vowelhfreq))

	pad = 100
	
	
	freqStable = stablePoint(conshfreq, 0, 100, 20, pad)		#find the stable point of the frequency
	magStable =  stablePoint(conshmag, 0, 40, 10, pad)		#find the stable point of the magnitude
	print freqStable, magStable
	stable = max(freqStable, magStable)				#find the stable point of both frequency and magnitude
	print conshfreq.shape[0]
	if stable == conshfreq.shape[0]+pad:
		stable = min(freqStable, magStable)
	print stable 
	
	adjustMagnitude(conshmag, vowelhmag, stable, vowelPadF)

	consFreqF0 = infoAt(conshfreq, stable)				#find the f0 frequency of the consonant at the stable point
	vowelFreqF0 = infoAt(vowelhfreq, 1.0*framesPerSecond(vowelFS, samplesPerFrame(vowelX, vowelhfreq)))
	print "consFreq:",consFreqF0
	print "vowelFreq:",vowelFreqF0
	pR = pitchRatio(consFreqF0, vowelFreqF0)			#find the pitch ration between the frequencies
	#print pR
	#print soundLength(consX, consFS), numFrames(conshfreq)
	initialNumFrames = numFrames(conshfreq)
	if pR != 1:
		consX = retune(consFS, consX, 1.0/pR)				#stretch or shrink the consonant as necessary
	
	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS)#re-harmonic-ize the consonant
	afterRetuneNumFrames = numFrames(conshfreq)
	stable = int(stable*(float(afterRetuneNumFrames)/initialNumFrames))#calculate where the stable frame is after the retune
	#print stable, newStable
	consFreqF0 = infoAt(conshfreq, stable)				#find the new frequency at the new stable point
	#print soundLength(consX, consFS), numFrames(conshfreq)
	#print pitchRatio(consFreqF0, vowelFreqF0)
	print stable
	print "fps",framesPerSecond2(soundLength(consX, consFS), numFrames(conshfreq))

	padAmount = 1000 - (stable*samplesPerFrame(consX, conshfreq)/consFS)*1000
														#set pad amount to line up the consonant \/ \/ \/ \/
	consX, consFS = zeroPad(consX, consFS, padAmount)			#add enough samples to put the cut point at 1 second into consonant
	#print padAmount* 
	#print phaseAt(conshphase, stable)					#this works because conssphase has not been changed to reflect the pad amount yet
	#print phaseAt()

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS)
														#construct harmonic arrays from paddedconsonant sound
	stable += padAmount/1000*framesPerSecond2(soundLength(consX, consFS), numFrames(conshfreq))
	print stable
	consPhase = infoAt(conshphase, 1.0*framesPerSecond(consFS, samplesPerFrame(consX, conshfreq)))
	vowelPhase = infoAt(vowelhphase, 1.0*framesPerSecond(vowelFS, samplesPerFrame(vowelX, vowelhfreq)))
	
	consFreqF0 = infoAt(conshfreq, 1.0*framesPerSecond(consFS, samplesPerFrame(consX, conshfreq)))
	sf.write("output_sounds/Cons.wav", consX, consFS)
	simpleXFade(consX, vowelX, consFS, stable, 10000, conshfreq)
	#print f0phaseShiftAmount(consPhase, vowelPhase, consFS, consFreqF0)
	print "elapsed time: {}".format(time.time()-startTime)
if __name__ == '__main__':
	main()