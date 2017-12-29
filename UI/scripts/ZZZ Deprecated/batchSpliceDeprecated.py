import soundOps
import os
from os.path import isfile, join


import subprocess
import time
import getch
import imp
#fn = f0 * (a)^n where a = 2^1/12 
def getApproxTones(startFreq, length):
	a = 2**(1.0/12)
	freqList = [startFreq]
	for i in range(1,length):
		#print freqList[0]
		#*(a**i)
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


def indiv():
	pass

def getSlope(x1,y1,x2,y2):
	return (float(y2)-y1)/(float(x2)-x1)
def translatePoint(n,numFiles, length=200.0):
	return n*length/numFiles

def getPad(translatedPoint,slope,basePoint):
	return slope*(translatedPoint-basePoint[0])+basePoint[1]

def s():
	pass

def batch(settings):

	consFolder = settings["consFolder"]
	vowelFolder = settings["vowelFolder"]
	outDirectory =  settings["outFolder"]
	startFreq =  int(settings["initial frequency"])
	cfL =  int(settings["xFade Length"])
	vowelPadMs =  int(settings["Vowel Pad"])
	splicePointMs =  int(settings["Splice Point"])
	InitPad =  int(settings["InitPad"])
	EndPad = int(settings["EndPad"])
	soundBounds = float(settings["Tuning Bounds"])
	Ns = 512#settings[""]
	H = 128#settings[""]

	slope = getSlope(0,InitPad,200,EndPad)
	if not os.path.exists(outDirectory): os.makedirs(outDirectory);
	
	if consFolder[-1] == " ":
		consFolder = consFolder[:-1]
	consFiles = [consFolder+"/"+f for f in os.listdir(consFolder) if isfile(join(consFolder, f)) and not f.startswith('.')]
	
	
	if vowelFolder[-1] == " ":
		vowelFolder = vowelFolder[:-1]
	vowelFiles = [vowelFolder+"/"+f for f in os.listdir(vowelFolder) if isfile(join(vowelFolder, f)) and not f.startswith('.')]

	fList = getApproxTones(startFreq, len(consFiles))
	redoList = []
	
	names = []
	print "----------",InitPad,EndPad
	print "----------",slope
	for i in range(len(fList)):
		translatedPoint = translatePoint(i ,len(fList))
		pad = getPad(translatedPoint,slope,(0,InitPad))
		print "++++++++++++++", pad
		bounds = getBounds(fList[i], soundBounds)#
		name = getName(consFiles[i], vowelFiles[i]) #
		name = outDirectory+"/" + name#
		print name
		soundOps.splice(consFiles[i], vowelFiles[i], cfL, pad, vowelPadMs, splicePointMs, bounds[0], bounds[1], name, Ns=512, H=128)
		names.append(name)
	#print "\a"
	return names
def main():
	pass
	#spliceBatch("../Morgan_44.1/Talk","../Morgan_44.1/Ah Main", "testDirectory", 87)
	#spliceIndividual("/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Talk/Talk_06.wav","/Users/backup/Desktop/gits/SpliceTools/Morgan_44.1/Ah Main/Ah Main_06.wav", "testDirectory", 120)
if __name__ == '__main__':
	main()