from attack import *
import numpy as np
import trim as T
import os, math
import interpolators

class Splice:
	def __init__(self):
		#self.toneFile = toneFile
		#self.attackFile = attackFile
		self.toneFileList = []
		self.attackFileList = []

		self.xF = 200


		self.Ns = 512
		self.H = 128
		#set arrays of sounds
		#self.init()
		#trim tones accordingly
		#self.trimAttack()
		#if trimTone:
		#self.trimTone(200)
		#re-Construct np arrays for retuning and splicing
		#self.re_init()
		#find correctionValue
		#print self.pitchRatio()
		#reTune the attack:
		#self.retuneAttack(1.0/self.pitchRatio())
		#self.re_init()
		#print self.pitchRatio()

		#self.xFF = 44100/float(self.hfreqA.shape[0])*self.xF

		#self.splice()
	def getLatestAttack(self):
		return self.attackFileList[-1]
	def getLatestTone(self):
		return self.toneFileList[-1]

	def setXF(self, xF):
		self.xF = xF

	def init(self):
		"""
		constructs np arrays of the sounds
		"""
		(self.hfreqA, self.hmagA, self.hphaseA, self.xrA, self.fsA, self.xA )= construct(self.attackFile)
		(self.hfreqT, self.hmagT, self.hphaseT, self.xrT, self.fsT, self.xT)  = construct(self.toneFile)

		if self.fsA != self.fsT:
			raise ValueError("Please use files with matching Sample Rates")

		self.xFF = self.fsA/float(self.hfreqA.shape[0])*self.xF

	def re_init(self):
		"""
		re-Constructs np arrays of the latest sounds
		"""
		self.hfreqA, self.hmagA, self.hphaseA, self.xrA, self.fsA, self.xA = construct(self.attackFileList[-1])
		self.hfreqT, self.hmagT, self.hphaseT, self.xrT, self.fsT, self.xT = construct(self.toneFileList[-1])
		print "len:", self.xA.shape

	def trimPoint(self):
		hfreqAttack = cutPoint(self.hfreqA, 4, 50, 20)
		hmagAttack = cutPoint(self.hmagA, 0, 1, 200)

		self.theCut = max(hfreqAttack, hmagAttack)
	#def trimAttack(self):
		"""
		trims the attack
		"""
		self.clippedAttack = 'output_sounds/' + os.path.basename(self.attackFile)[:-4] + '_clippedAttack.wav'
		self.attackFileList.append(self.clippedAttack)
		hfreqAttack = cutPoint(self.hfreqA, 4, 50, 20)
		hmagAttack = cutPoint(self.hmagA, 0, 1, 200)

		theCut = max(hfreqAttack, hmagAttack)
		yAttack = makeSound(self.hfreqA, self.hmagA, self.hphaseA, self.xrA, self.Ns, self.H, self.fsA, theCut, 10+self.xF*0.75)
		writeSound(yAttack, self.fsA, self.clippedAttack)


	def attack(self, attackFile):
		self.attackFile = attackFile
		self.attackFileList.append(self.attackFile)
	def tone(self, toneFile):
		self.toneFile = toneFile
		self.toneFileList.append(self.toneFile)


	def trimTone(self, trimAmount, backEnd = 4000):
		"""
		trims the front of the tone
		"""

		self.clippedTone = 'output_sounds/' + os.path.basename(self.toneFile)[:-4] + '_clipped.wav'
		self.toneFileList.append(self.clippedTone)
		T.slice(self.toneFile, self.clippedTone, trimAmount, backEnd)

	def playBack(self, which):
		"""
		plays back tones... needs work
		"""
		if which == "a":
			playFile = self.attackFile
		elif which == "t":
			playFile = self.toneFile
		elif which == "c":
			playFile = self.clippedTone
		elif which == "l":
			playFile = self.toneFileList[-1]
		os.system("afplay "+playFile.replace(" ", "\\ "))

	def retuneAttack(self, sR, mode = "linear"):
		"""
		sR: stepRatio
		"""

		self.retunedAttack = 'output_sounds/' + os.path.basename(self.attackFile)[:-4] + '_retuned.wav'
		self.attackFileList.append(self.retunedAttack)

		yRetuned = interpolators.linear(self.clippedAttack, sR)
		writeSound(yRetuned, self.fsA, self.retunedAttack)

	def ptFreq(self, hfreq, n, pt):
		"""
		hfreq: np array of harmonic frequencies
		n: which harmonic(0 for f0)
		pt: location in sound
		returns: frequency of harmonic at point
		"""
		return hfreq[pt, n]

	def pitchRatio(self):
		"""
		returns ratio of pitches
		"""
		#print self.hfreqA[-1, 0]
		#print self.hfreqT[0,0]
		print self.xF
		print self.hfreqA.shape
		return self.hfreqA[self.theCut-self.xF/2, 0]/self.hfreqT[self.xF/2,0]

	def phaseAdjust(self):
		print "===phase==="
		phase1 = self.hphaseA[self.theCut, 0]#%math.pi
		phase2 = self.hphaseT[0, 0]#%math.pi
		print "phase1:", phase1
		print "phase2:", phase2
		spw = self.fsA/self.hfreqT[0,0] #number of samples in a wave cycle

		twoPI = 2*math.pi

		deltaPh = twoPI-phase1+phase2

		framesToAdd = (deltaPh*spw)/twoPI
		print framesToAdd
		arr = np.zeros(int(framesToAdd))
		self.xA = np.concatenate((arr, self.xA))

		self.phasedAttack = 'output_sounds/' + os.path.basename(self.attackFile)[:-4] + '_phased.wav'
		self.attackFileList.append(self.phasedAttack)


		writeSound(self.xA, self.fsA, self.phasedAttack)


	def splice(self):
		"""
		splices two files together
		"""
		T.xFade(self.attackFileList[-1], self.toneFileList[-1], int(self.xFF))


def main():
	splice = Splice()
	splice.attack("/Users/backup/Desktop/gits/SpliceTools/sounds/PattyMee_00.wav")
	splice.tone("/Users/backup/Desktop/gits/SpliceTools/sounds/PattyEe_00.wav")
	splice.init()
		#trim tones accordingly
	splice.trimPoint()
		#if trimTone:
	splice.trimTone(200)
		#re-Construct np arrays for retuning and splicing
	splice.re_init()
		#find correctionValue
	print splice.pitchRatio()
		#reTune the attack:
	splice.retuneAttack(1.0/splice.pitchRatio())
	splice.re_init()
	print splice.pitchRatio()
	splice.phaseAdjust()
	splice.re_init()
	#splice.phaseAdjust()
	splice.splice()


if __name__ == '__main__':
	main()


