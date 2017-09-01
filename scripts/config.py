"""
Welcome to the settings file for batchSplice
Here you will fined the basic settings for splicing
the two files together
TO EDIT THIS FILE: press a(for insert mode)
TO SAVE THESE SETTINGS: press ESQ,
then ":wq"
"""
class Config:
	def __init__(self):
		'''soundOps Stability Preferences'''
		self.freqSurveyDepth = 0		#which harmonic to sample
		self.freqThreshold = 20			#how much the frequency can differ
		self.freqStabilityValue = 10 	#how long to test the sound

		self.magSurveyDepth = 0			#which harmonic to sample
		self.magThreshold = 40			#how much the frequency can differ
		self.magStabilityValue = 10 	#how long to test the sound

		self.endingCutoff = 0.5			#a backup just in case no stability is detected
										#this is a fraction of the consonant

		'''batchSplice Preferences'''
		#default: 1000
		self.cfL = 1000					#cross fade length in samples
		#default: 20
		self.pad = 30					#the pad amount added after a stable
										#point is found
		#default: 700
		self.vowelPadMs = 700			#how long to pad the vowel

		#default: 0.3
		self.soundBounds = 0.3 			#size of the bounds for the fourier
										#transform
		'''Individual Versions:
		Edit these after going
		through the batch splice'''
		self.IcfL = 1000
		self.Ipad = 20
		self.IvowelPadMs = 700
        
													
										
		
