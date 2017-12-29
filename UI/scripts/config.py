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
		'''soundOps Stability Preferences CHANGE THESE'''
		self.freqSurveyDepth = 5		#how many harmonics to sample
		self.freqThreshold = 0.5		#how much the frequency can differ
		self.freqStabilityValue = 20 	#how long to test the sound
		self.magThreshold = 50			#how much the magnitude can differ

		
        
													
										
		
