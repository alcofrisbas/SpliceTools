import numpy as np
import soundfile as sf
import time
import math
import matplotlib.pyplot as plt


from scipy.signal import get_window

from models import hprModel as HPR
import config

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
        try:
        	newsound[i] += y[intItemp] + xfrac * (y[intItemp+1]-y[intItemp])
        except:
        	print "wtf"
    arr = np.asarray(newsound)
    return np.float32(arr)/norm_fact[arr.dtype.name]

							#returns frames per second using another method
#doubled M and N to make it work.... 
def fourierResidual(x, fs, minf0, maxf0, window='blackman', M=1201, N=2048, t=-100, minSineDur=0.1, nH=20,  f0et=5, harmDevSlope=0.01):
	Ns = 512											#
	H = 128												#hop size

	w = get_window(window, M)							#get analysis window
	hfreq, hmag, hphase, xr = HPR.hprModelAnal(x, fs, w, N, H, t, minSineDur, nH, minf0, maxf0, f0et, harmDevSlope)
	return hfreq, hmag, hphase, xr						#returns 2D arrays and 1D array of residual sound

'''def stablePoint(inHarmonicArray, surveyDepth, threshold, stabilityValue, pad):
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
		values = []
		#print inHarmonicArray[i, surveyDepth]										#empty list of error values
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
	return cutPoint+pad'''

def stablePoint(hfreqArray, hmagArray, FreqThreshold,  MagThreshold, surveyDepth, windowLength, v):
	"""
	inHarmonicArray: hfreq or hmag
	surveyDepth: which harmonic to test for stability
	threshold: error threshold
	stabilityValue: number of frames to test for stability
	"""
	surveyLen = hfreqArray.shape[0]				#duration of sound for for loop
	cutPoint = surveyLen 								#sets default cutPoint just in case none is found
	
	
	for i in range(surveyLen-windowLength):
		if v:
			print i
		isCut = True
		for h in range(surveyDepth):
			if not isCut:
				break									#indicator that a cut point has been found
			values = []
			#print inHarmonicArray[i, surveyDepth]										#empty list of error values
			for j in range(1,windowLength-1):								#compares array values with values j ahead and logs error values
				initValFreq = hfreqArray[i, h]
				compValFreq = hfreqArray[i+j, h]
				initValMag = hmagArray[i, h]
				compValMag = hmagArray[i+j, h]
				if initValFreq == 0:
					if h == 0:
						freqError = 1000
				else:
					freqError = np.abs((float(initValFreq)/compValFreq)-1)
				magError = np.abs(initValMag - compValMag)
				if v:
					print h, j, freqError, magError
				if (freqError > FreqThreshold or initValFreq == 0) or (magError > MagThreshold or initValMag == 0):
					isCut = False
					break

		if isCut:
			cutPoint = i
			return cutPoint
	return i

def errorValues(hfreqArray, hmagArray):
	"""
	inHarmonicArray: hfreq or hmag
	surveyDepth: which harmonic to test for stability
	threshold: error threshold
	stabilityValue: number of frames to test for stability
	"""
	surveyLen = hfreqArray.shape[0]				#duration of sound for for loop
	cutPoint = surveyLen 								#sets default cutPoint just in case none is found
	freqErrorValues = []
	magErrorValues = []
	surveyDepth = hfreqArray.shape[1]
	
	for i in range(surveyLen-1):
		freqList = []
		magList = []
		for h in range(surveyDepth):
			initValFreq = hfreqArray[i, h]
			compValFreq = hfreqArray[i+1, h]
			initValMag = hmagArray[i, h]
			compValMag = hmagArray[i+1, h]
			if compValFreq == 0:
				freqError = 1000
			else:
				freqError = np.abs((float(initValFreq)/compValFreq)-1)
			magError = np.abs(initValMag - compValMag)
			freqList.append(freqError)
			magList.append(magError)
		
		freqErrorValues.append(freqList)
		magErrorValues.append(magList)
	return np.array(freqErrorValues), np.array(magErrorValues)


def adjustPhase(H, consFS, conshfreq, conshphase, cfLF, swF, vowelhphase):
	HopTime = float(H)/consFS
	if conshfreq[swF, 1] == 0:
		return
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
		top = conshmag[stable, i]
		bottom = vowelhmag[stable+vowelPadF, i]
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

def getInfo(consFile, f0min, f0max, H=512):
	consX, consFS = soundToArray(consFile)				#read file to array
	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, f0min, f0max)
	plt.figure()

	maxplotfreq = 5000.0
	for i in conshfreq:
		print i

	# plot the input sound
	plt.subplot(4,1,1)
	plt.plot(np.arange(consX.size)/float(consFS), consX)
	plt.axis([0, consX.size/float(consFS), min(consX), max(consX)])
	plt.ylabel('amplitude')
	plt.xlabel('time (sec)')
	plt.title(consFile+" "+str(f0min)+" "+str(f0max))

	# plot the magnitude spectrogram of residual
	plt.subplot(4,1,2)
	'''maxplotbin = int(N*maxplotfreq/consX)
	numFrames = int(mXr[:,0].size)
	frmTime = H*np.arange(numFrames)/float(fs)                       
	binFreq = np.arange(maxplotbin+1)*float(fs)/N                         
	plt.pcolormesh(frmTime, binFreq, np.transpose(mXr[:,:maxplotbin+1]))
	plt.autoscale(tight=True)
	'''
	# plot harmonic frequencies on residual spectrogram
	if (conshfreq.shape[1] > 0):
		harms = conshfreq*np.less(conshfreq,maxplotfreq)
		harms[harms==0] = np.nan
		numFrames = int(harms[:,0].size)
		frmTime = H*np.arange(numFrames)/float(consFS) 
		plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
		plt.xlabel('time(s)')
		plt.ylabel('frequency(Hz)')
		plt.autoscale(tight=True)
		plt.title('harmonics')
	plt.subplot(4,1,3)
	if (conshmag.shape[1] > 0):
		harms = conshmag*np.less(conshmag,0)
		harms[harms==0] = np.nan
		numFrames = int(harms[:,0].size)
		frmTime = H*np.arange(numFrames)/float(consFS) 
		plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
		plt.xlabel('time(s)')
		plt.ylabel('amplitude')
		plt.autoscale(tight=True)
		plt.title('amplitude')
	# plot the output sound
	plt.subplot(4,1,4)
	plt.plot(np.arange(consxr.size)/float(consFS), consxr)
	plt.axis([0, consxr.size/float(consFS), min(consxr), max(consxr)])
	plt.ylabel('amplitude')
	plt.xlabel('time (sec)')
	plt.title('output sound: y')
	
	#plt.tight_layout()
	plt.show()

def graphError(consFile, f0min, f0max, Ns=512, H=128):
	c = config.Config()
	consX, consFS = soundToArray(consFile)				#read both files to arrays

	
	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, f0min, f0max)
														#using SMS Tools, construct arrays
														#of the components of each sound
	
	hfreqError, hmagError = errorValues(conshfreq, conshmag)
	
	maxplotfreq = 60
	plt.figure()
	plt.subplot(2,1,1)
	if (hfreqError.shape[1] > 0):
		harms = hfreqError*np.less(hfreqError,maxplotfreq)
		harms[harms==0] = np.nan
		numFrames = int(harms[:,0].size)
		frmTime = H*np.arange(numFrames)/float(consFS) 
		plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
		plt.xlabel('time(s)')
		plt.ylabel('frequency(Hz)')
		plt.autoscale(tight=True)
		plt.title('frequency error')

	plt.subplot(2,1,2)
	if (hmagError.shape[1] > 0):
		harms = hmagError*np.less(hmagError,maxplotfreq)
		harms[harms==0] = np.nan
		numFrames = int(harms[:,0].size)
		frmTime = H*np.arange(numFrames)/float(consFS) 
		plt.plot(frmTime, harms, color='k', ms=3, alpha=1)
		plt.xlabel('time(s)')
		plt.ylabel('some number')
		plt.autoscale(tight=True)
		plt.title('mag error')
	plt.tight_layout()
	plt.show()



def splice(consFile, vowelFile, cfL, pad, vowelPadMs, splicePointMs, f0min, f0max, outFile,Ns=512, H=128):
	c = config.Config()
	consX, consFS = soundToArray(consFile)				#read both files to arrays
	vowelX, vowelFS = soundToArray(vowelFile)			#and capture their sample rate

	if consFS != vowelFS:								#make sure that sample rates match
		raise ValueError("Please use samples with matching Sample Rates")

	vowelX, vowelFS = zeroPad(vowelX, vowelFS, 700)		#rewrite the vowel file with
														#a pad of VOWELPADMS ms

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS, f0min, f0max)
	vowelhfreq, vowelhmag, vowelhphase, vowelxr = fourierResidual(vowelX, vowelFS, f0min, f0max)
														#using SMS Tools, construct arrays
														#of the components of each sound
	vowelPadF = (vowelPadMs/1000.0)*framesPerSecond2(soundLength(vowelX, vowelFS), numFrames(vowelhfreq))
														#the vowel pad in Frames(vs samples or ms)
	cfLF = cfL/samplesPerFrame(consX, conshfreq)		#cfL in Frames(vs samples)
	#hfreqArray, hmagArray, FreqThreshold,  MagThreshold, surveyDepth, windowLength, verbose
	stable = stablePoint(conshfreq, conshmag, c.freqThreshold,  c.magThreshold, c.freqSurveyDepth, c.freqStabilityValue, False)+ pad
	if stable >= conshfreq.shape[0]:
		stable = conshfreq.shape[0]-1

	'''stable = max(freqStable, magStable)					#take the maximum for stable point
				if stable == conshfreq.shape[0]+pad:				#However, the highest never detects one
					print "None found in Frequency"
					stable = min(freqStable, magStable)				#use the lower value
				#print freqStable, magStable, conshfreq.shape[0]
				if stable >= conshfreq.shape[0]:
					errorString = "No stable point was found with the current settings.\nPlease change these settings in config.py"
					stable = conshfreq.shape[0]*c.endingCutoff
					print errorString'''
	zerosFreq = 0
	zerosMag = 0
	for i in range(conshfreq.shape[0]):
		if conshfreq[i, 0] != 0:
			zerosFreq += 1
		if conshmag[i,0] != 0:
			zerosMag += 1
	#print "Frequency Stable: {0} Amplitude Stable: {1}".format(freqStable, magStable)
	adjustMagnitude(conshmag, vowelhmag, stable, vowelPadF)#adjusts the magnitudes of each harmonic
														#to match with the vowel's harmonics

	consFreqF0 = infoAt(conshfreq, stable)				#find the f0 frequency of the consonant at the stable point
	vowelFreqF0 = infoAt(vowelhfreq, 1.0*framesPerSecond(vowelFS, samplesPerFrame(vowelX, vowelhfreq)))
														#find the f0 frequency of the vowel at the stable point
	pR = pitchRatio(consFreqF0, vowelFreqF0)			#find the pitch ration between the frequencies
	initialNumFrames = numFrames(conshfreq)				#number of frames in the consonant sound

	if pR != 1:											#stretch or shrink the consonant as necessary
		consX = retune(consFS, consX, 1.0/pR)			#to match its pitch to the vowel's

	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS,f0min ,f0max)
														#re-harmonic-ize the consonant
	afterRetuneNumFrames = numFrames(conshfreq)			#the duration in Frames of the consonant after the stretch

	stable = int(stable*(float(afterRetuneNumFrames)/initialNumFrames))#calculate where the stable frame is after the retune
	consFreqF0 = infoAt(conshfreq, stable)				#find the new frequency at the new stable point

	padAmount = splicePointMs - (stable*samplesPerFrame(consX, conshfreq)/consFS)*1000
														#set pad amount to line up the consonant \/ \/ \/ \/
	consX, consFS = zeroPad(consX, consFS, padAmount)	#add enough samples to put the cut point at 1 second into consonant
	conshfreq, conshmag, conshphase, consxr = fourierResidual(consX, consFS,f0min, f0max)
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
	writeSound(outFile, newX, consFS)


def main():
	getInfo("../Morgan_44.1/Mod/Mod_20.wav", 200, 300)
	#splice("../Morgan_44.1/Mod/Mod_20.wav", "../Morgan_44.1/Ah Main/Ah Main_20.wav", 1000, 25, 700, 200, 300, "01Test.wav", Ns=512, H=128)
if __name__ == '__main__':
	main()