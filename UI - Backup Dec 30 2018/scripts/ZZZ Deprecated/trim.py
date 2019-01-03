import wave
from scipy.io.wavfile import write, read
import numpy as np

from models import utilFunctions as UF
import soundfile as sf

INT16_FAC = (2**15)-1
INT32_FAC = (2**31)-1
INT64_FAC = (2**63)-1
norm_fact = {'int16':INT16_FAC, 'int32':INT32_FAC, 'int64':INT64_FAC,'float32':1.0,'float64':1.0}


def slice(infilename, outfilename, start_ms, end_ms):
    infile = wave.open(infilename, "r")
    width = infile.getsampwidth()
    rate = infile.getframerate()
    fpms = rate / 1000 # frames per ms
    length = (end_ms - start_ms) * fpms
    start_index = start_ms * fpms

    out = wave.open(outfilename, "w")
    out.setparams((infile.getnchannels(), width, rate, length, infile.getcomptype(), infile.getcompname()))
    
    infile.rewind()
    anchor = infile.tell()
    infile.setpos(anchor + start_index)
    out.writeframes(infile.readframes(length))

def xFade(infilename1, infilename2, length):
    

    #fs1, x1 = UF.wavread(infilename1)

    (x1, fs1) = sf.read(infilename1)
    x1 = np.float32(x1)/norm_fact[x1.dtype.name]

    (x2, fs2) = sf.read(infilename2)
    
    x2 = np.float32(x2)/norm_fact[x2.dtype.name]

    print x2.shape
    for i in range(0, length):
        #print i
        #print x2[i]
        #print i, length/2
        #print (float(i)/(length/2))
        #print x2[i]
        x2[i] = x2[i]*(float(i)/(length))

    pad = np.zeros(len(x1)-length)#len(x1))
    finalTone = np.concatenate((pad, x2), axis=0)
    
    print x2.shape
    print finalTone.shape
    print "testing"
    for i in range(-1, (-1*length), -1):
        x1[i] = x1[i]*(float(i)/(-1*length))

    UF.wavwrite(x1, fs1, "test1.wav")

    UF.wavwrite(x2, fs2,"test2.wav")
    diff = finalTone.shape[0] - x1.shape[0]
    finalAttack = np.concatenate((x1, np.zeros(diff)), axis=0)
    print x1.shape
    print finalAttack.shape
    x3 = np.add(finalAttack, finalTone)

    UF.wavwrite(x3, fs2,"test3.wav")



def phaseAdjust():
    pass




    
if __name__ == "__main__":
    xFade("/Users/backup/Desktop/gits/SpliceTools/scripts/output_sounds/PattyMee_00_retuned.wav","/Users/backup/Desktop/gits/SpliceTools/scripts/output_sounds/PattyEe_00_clipped.wav",10000)
    #slice(wave.open("/Users/backup/Desktop/gits/SpliceTools/sounds/PattyMee_00.wav", "r"), "test.wav", 500, 30000)