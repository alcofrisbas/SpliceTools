import soundOps
import os
from os.path import isfile, join


import subprocess
import time
import getch
import imp
#fn = f0 * (a)^n where a = 2^1/12 
def getApproxTones(startFreq, l):
	a = 2**(1.0/12)
	freqList = [startFreq]
	for i in range(1,l):
		freqList.append(freqList[0]*(a**i))
	return freqList

def getBounds(tone, boundAmount):
	bound = tone*boundAmount
	return (tone-bound, tone+bound)

def getName(consFile, vowelFile):
	num = getNum(consFile, vowelFile)
	return consFile.split("/")[-1].split("_")[0]+"+"+vowelFile.split("/")[-1].split("_")[0]+"_"+num+".wav"

def getNum(consFile, vowelFile):
	consInit = consFile.split("/")[-1].split("_")[-1][:-4]
	vowelInit = vowelFile.split("/")[-1].split("_")[-1][:-4]
	if consInit == vowelInit:
		return consInit
	errorString = "Please Provide Batch Folders with matching Notes... \n your first conosonant is {0} and your first vowel is {1}".format(consInit, vowelInit)
	raise ValueError(errorString)
def editConfig():
	os.system("vi config.py")
	import config
	config = reload(config)
	c = config.Config()
	return c

def spliceIndividual(consFile, vowelFile, outDirectory,freq):
	if not os.path.exists(outDirectory): os.makedirs(outDirectory);
	import config
	c = config.Config()
	#c = editConfig()
	bounds = getBounds(freq, c.soundBounds)
	name = getName(consFile, vowelFile)
	name = outDirectory+"/" + name
	soundOps.splice(consFile, vowelFile, c.cfL, c.pad, c.vowelPadMs, c.splicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)

def spliceBatch(consFolder, vowelFolder, outDirectory, startFreq):
	if not os.path.exists(outDirectory): os.makedirs(outDirectory);#
	import config
	c = config.Config()
	#consFolder = "/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Zahz"
	if consFolder[-1] == " ":
		consFolder = consFolder[:-1]
	consFiles = [consFolder+"/"+f for f in os.listdir(consFolder) if isfile(join(consFolder, f)) and not f.startswith('.')]
	
	#vowelFolder = "/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Ah Main"
	if vowelFolder[-1] == " ":
		vowelFolder = vowelFolder[:-1]
	vowelFiles = [vowelFolder+"/"+f for f in os.listdir(vowelFolder) if isfile(join(vowelFolder, f)) and not f.startswith('.')]

	#startFreq = input("Enter the approximate frequency of the first tone: ")
	#splice(consFile, vowelFile, cfL, pad, vowelPadMs, f0min, f0max, Ns=512, H=128)
	fList = getApproxTones(startFreq, len(consFiles))
	redoList = []
	print "would you like to change presets: press y for yes; any other key for no"
	if getch.getch() == "y":
		c = editConfig()
	mode = "n"#normal
	print "press v for verbose mode, which enables flagging and individual editing"
	if getch.getch() == "v":
		mode = "v"
	for i in range(len(fList)):
		bounds = getBounds(fList[i], c.soundBounds)#
		name = getName(consFiles[i], vowelFiles[i]) #
		print name
		name = outDirectory+"/" + name#

		print fList[i], bounds[0], bounds[1]
		if mode == "v":
			if os.path.isfile(name):
				proc = subprocess.Popen(["afplay",name])
				time.sleep(2)
				proc.terminate()
			else:
				print "no file found, splicing"
				soundOps.splice(consFiles[i], vowelFiles[i], c.cfL, c.pad, c.vowelPadMs, c.splicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)#
			print "to flag this as unsatisfactory, press n\nTo play again, press r"
			f = getch.getch()
			if f == "n":
					print "adding"
					redoList.append([consFiles[i], vowelFiles[i]])
			while f == "r":
				proc = subprocess.Popen(["afplay", name])
				time.sleep(2)
				proc.terminate()
				print "to flag this as unsatisfactory, press n\nTo play again, press r"
				f = getch.getch()
				print "round 1", f
				if f == "n":
					print "adding"
					redoList.append([consFiles[i], vowelFiles[i]])
			print "s to skip splice process"
			if getch.getch() == "s":
				continue
			if f == "q":
				break
			soundOps.splice(consFiles[i], vowelFiles[i], c.cfL, c.pad, c.vowelPadMs, c.splicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)
		
		else:
			soundOps.splice(consFiles[i], vowelFiles[i], c.cfL, c.pad, c.vowelPadMs, c.splicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)
		
		'''if mode == "v":
			fullName = "output_sounds/"+ name
			print fullName
			proc = subprocess.Popen(["afplay",fullName])
			time.sleep(2)
			proc.terminate()
			print "to flag this as unsatisfactory, press n\nTo play again, press r"
			f = getch.getch()
			while f == "r":
				proc = subprocess.Popen(["afplay", fullName])
				time.sleep(2)
				proc.terminate()
				print "to flag this as unsatisfactory, press n\nTo play again, press r"
				f = getch.getch()
				if f == "n":
					redoList.append([consFiles[i], vowelFiles[i]])
			if f == "q":
				break'''
	if mode == "v":
		print redoList
		for i in redoList:
			print "to edit {}, press e".format(i)
			name = getName(i[0], i[1]) #print i, fList[i], bounds
			name = outDirectory+"/" + name
			
			print "editing {}".format(name)
			if getch.getch() == "e":
				c = editConfig()
				soundOps.splice(i[0], i[1], c.IcfL, c.Ipad, c.IvowelPadMs, c.IsplicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)
			proc = subprocess.Popen(["afplay",name])
			time.sleep(2)
			proc.terminate()
			print "to re-edit the settings, press e\nto play again, press r\nif you are satisfied, press y"
			f = getch.getch()
			while f == "e" or f == "r":
				if f == "e":
					c = editConfig
					soundOps.splice(i[0], i[1], c.IcfL, c.Ipad, c.IvowelPadMs, c.IsplicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)
				proc = subprocess.Popen(["afplay",name])
				time.sleep(2)
				proc.terminate()
				print "to re-edit the settings, press e\nto play again, press r\nif you are satisfied, press y"
				f = getch.getch()
	print "\a"

'''def prompt():
	consFolder = raw_input("Enter Consonant Folder: ").replace("\\", "")
	if consFolder[-1] == " ":
		consFolder = consFolder[:-1]
	consFiles = [consFolder+"/"+f for f in os.listdir(consFolder) if isfile(join(consFolder, f)) and not f.startswith('.')]
	
	vowelFolder = raw_input("Enter Vowel Folder: ").replace("\\", "")
	if vowelFolder[-1] == " ":
		vowelFolder = vowelFolder[:-1]
	vowelFiles = [vowelFolder+"/"+f for f in os.listdir(vowelFolder) if isfile(join(vowelFolder, f)) and not f.startswith('.')]
	
	startFreq = input("Enter the approximate frequency of the first tone: ")
	#splice(consFile, vowelFile, cfL, pad, vowelPadMs, f0min, f0max, Ns=512, H=128)
	fList = getApproxTones(startFreq, len(consFiles))
	
	for i in range(len(fList)):
		bounds = getBounds(fList[i], 0.2)
		name = getName(consFiles[i], vowelFiles[i]) #print i, fList[i], bounds
		name = "spliced/" + name
		print fList[i], bounds[0], bounds[1]
		soundOps.splice(consFiles[i], vowelFiles[i], 1000, 25, 700, bounds[0], bounds[1], name, Ns=512, H=128)'''
def main():
	#spliceBatch("../Morgan_44.1/Talk","../Morgan_44.1/Ah Main", "testDirectory", 87)
	spliceIndividual("/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Talk/Talk_06.wav","/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Ah Main/Ah Main_06.wav", "testDirectory", 120)
if __name__ == '__main__':
	main()