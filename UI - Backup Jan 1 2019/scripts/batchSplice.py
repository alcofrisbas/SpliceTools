import json
import os, sys
from os.path import isfile, join
import soundOps


def getSlope(x1,y1,x2,y2):
	return (float(y2)-y1)/(float(x2)-x1)

def translatePoint(n,numFiles, length=200.0):
	"""
	not sure here...
	"""
	return n*length/numFiles



def getApproxPitches(startFreq, length):
	"""
	This computes the frequencies of each of the notes
	returns: array of length :length:, containing
	frequencies of chromatic notes.
	"""
	a = 2**(1.0/12)
	freqList = [startFreq]
	for i in range(1,length):
		freqList.append(freqList[0]*(a**i))
	return freqList

def getPad(translatedPoint,slope,basePoint):
	"""
	padding for evenness
	"""
	return slope*(translatedPoint-basePoint[0])+basePoint[1]

def getName(consFile, vowelFile):
	"""
	given two filenames, return a wav filename with a merged name
	"""
	num = getNum(consFile, vowelFile)
	return consFile.split("/")[-1].split("_")[0]+"+"+vowelFile.split("/")[-1].split("_")[0]+"_"+num+".wav"

def getNum(consFile, vowelFile):
	"""
	return label number of two files...
	ex: bah_02.wav, ahh_02.wav returns "2"
	good for getting pitch given ~orig pitch and and
	how many steps above.
	if the numbers don't match, it raises an error.
	"""
	consInit = consFile.split("/")[-1].split("_")[-1][:-4]
	vowelInit = vowelFile.split("/")[-1].split("_")[-1][:-4]
	if consInit == vowelInit:
		return consInit
	errorString = "Please Provide Batch Folders with matching Notes... \n your first conosonant is {0} and your first vowel is {1}".format(consInit, vowelInit)
	raise ValueError(errorString)

def getBounds(tone, boundAmount):
	"""
	Return the uppper and lower bound of pitch for doing sound operations
	in a given sample... useful for sms tools ops.
	"""
	bound = tone*boundAmount
	return (tone-bound, tone+bound)



def setup(settings):
	"""
	given a dictionary of settings, set up the splicing environment for later use
	"""
	consFolder = settings["consFolder"]
	vowelFolder = settings["vowelFolder"]
	outDirectory =  settings["outFolder"]
	startFreq =  int(settings["initial frequency"])

	# =============== pad and cross fade length editing here - These values get overwritten by the UI
	InitPad =  00
	EndPad = 90
	icfL = 4000
	ecfL = 4000
	# ==============================================================
	padslope = getSlope(0,InitPad,200,EndPad)
	cfLslope = getSlope(0,icfL,200,ecfL)
	
	try:
		if not os.path.exists(outDirectory): os.makedirs(outDirectory);
	except Exception as e:
		print("improperly configured directories, please delete settings.json.")
		sys.exit(1)

	if consFolder[-1] == " ":
		consFolder = consFolder[:-1]
	consFiles = [consFolder+"/"+f for f in os.listdir(consFolder) if isfile(join(consFolder, f)) and not f.startswith('.')]


	if vowelFolder[-1] == " ":
		vowelFolder = vowelFolder[:-1]
	vowelFiles = [vowelFolder+"/"+f for f in os.listdir(vowelFolder) if isfile(join(vowelFolder, f)) and not f.startswith('.')]

	fList = getApproxPitches(startFreq, len(consFiles))
	pads = []
	cflList = []
	outFiles = []
	for i in range(len(fList)):
		translatedPoint = translatePoint(i ,len(fList))
		pad = getPad(translatedPoint,padslope,(0,InitPad))
		pads.append(pad)

		cfL = getPad(translatedPoint,cfLslope,(0,icfL))
		cflList.append(cfL)

		name = getName(consFiles[i], vowelFiles[i]) #
		name = outDirectory+"/" + name#
		outFiles.append(name)
	"""
	confiles is a list of paths to the consonant wav files(not the files themselves)
	same for vowels and outs.
	pads are values from UI
	freqs: a list of generated frequencies(based on starting freq and getApproxPitches, from UI, not WAV files.)
	cfls: a list of crossfade lengths from UI.
	"""
	return {"consFiles":consFiles,"vowelFiles":vowelFiles,"outFiles":outFiles, "pads":pads,"freqs":fList,"cfls":cflList}

def splice(i, setupOut, settings):
	# to edit the source folders and other main settings
	# type ./editsettings into the terminal
	print "============================================"
	print "============ PROCESS FILE #", i," ============="
	print "============================================"
	vowelPadMs =  int(settings["Vowel Pad"])
	splicePointMs =  int(settings["Splice Point"])
	soundBounds = float(settings["Tuning Bounds"])
	bounds = getBounds(setupOut["freqs"][i], soundBounds)
	print "   NOW WE START soundops.splice"
	print "========================="
	soundOps.splice(setupOut["consFiles"][i], setupOut["vowelFiles"][i], setupOut["cfls"][i], setupOut["pads"][i], vowelPadMs, splicePointMs, bounds[0], bounds[1], setupOut["outFiles"][i], Ns = 512, H = 128)
	print "   FINISHED WITH soundops.splice"
	print "  "
	print "setupOut[outfiles][i] = ", setupOut["outFiles"][i]
	print "CFL::::::: setupOut[cfls][i] = ",setupOut["cfls"][i]

	

if __name__ == '__main__':
	settings = json.loads(open('../settings.json').read())
	s = setup(settings)
	for i in range(27):
		splice(i, s, settings)
