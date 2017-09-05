"""
Welcome to the settings file for batchSplice
Here you will fined the basic settings for splicing
the two files together
TO EDIT THIS FILE: press a(for insert mode)
TO SAVE THESE SETTINGS: press ESQ,
then ":wq"
"""
#hfreqArray, hmagArray, FreqThreshold,  MagThreshold, surveyDepth, windowLength, verbose
#	stable = stablePoint(conshfreq, conshmag, 0.1,  50, 5, 20, True)+ pad
class Config:
	def __init__(self):
		'''soundOps Stability Preferences'''
		self.freqSurveyDepth = 5		#which harmonic to sample
		self.freqThreshold = 0.1			#how much the frequency can differ
		self.freqStabilityValue = 20 	#how long to test the sound

		self.magThreshold = 50			#how much the frequency can differ

		'''batchSplice Preferences'''
		#default: 1000
		self.cfL = 700					#cross fade length in samples
		#default: 20
		self.pad = 0					#the pad amount added after a stable
										#point is found
		#default: 700
		self.vowelPadMs = 700			#how long to pad the vowel

		#default: 1000
		self.splicePointMs = 1000

		#default: 0.3
		self.soundBounds = 0.3 			#size of the bounds for the fourier
										#transform
		'''Individual Versions:
		Edit these after going
		through the batch splice'''
		self.IcfL = 1000
		self.Ipad = 20
		self.IvowelPadMs = 700
		self.IsplicePointMs = 1000
        
													
										
		
