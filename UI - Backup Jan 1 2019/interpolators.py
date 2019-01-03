import os, sys
reload(sys)
sys.setdefaultencoding("utf-8")
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '/Users/backup/Desktop/sms-tools-master/software/models/'))
import utilFunctions as UF
'''infile = raw_input("Enter File: ")[:-1]
stepRatio = input("Enter step: ")
(fs, y) = UF.wavread(infile)
print infile, stepRatio, fs
#print y
lastI = len(y)/float(stepRatio)
T = []
for i in range(len(y)):
    T.append(i/float(fs))
for i in range(len(y)):
    if y[i] == 0:
        print "zero at "+str(i)
#plt.plot(T, y)
#plt.axis([0, 10000, -0.4, .4])
#print T
#plt.show()'''
def linear(infile, stepRatio):
    (fs, y) = UF.wavread(infile)
    lastI = len(y)/float(stepRatio)
    newsound = []
    for i in range(int(lastI+1)):
        newsound.append(0)
    for i in range(int(lastI)):
        iTemp = stepRatio*i
        intItemp = int(iTemp)
        xfrac = iTemp - intItemp
        newsound[i] += y[intItemp] + xfrac * (y[intItemp+1]-y[intItemp])
    return newsound

def Bspline4_3(infile, stepRatio):
    (fs, y) = UF.wavread(infile)
    lastI = len(y)/float(stepRatio)
    newsound = []
    for i in range(int(lastI+2)):
        newsound.append(0)
    for i in range(1, int(lastI-2)):
        iTemp = stepRatio*i
        intItemp = int(iTemp)
        xfrac = iTemp - intItemp
        m1p1 = float(y[intItemp-1]+y[intItemp+1])
        #print m1p1
        y0 = y[intItemp]
        c1v = y[intItemp+1]-y[intItemp-1]
        c2v = m1p1
        c3v1 = y[intItemp]-y[intItemp-1]
        c3v2 = y[intItemp+2]-y[intItemp-1]
        c0 = 1/6.0*m1p1 + 2/3.0*y0
        c1 = 1/2.0*c1v
        c2 = 1/2.0*c2v - y[intItemp]
        c3 = 1/2.0*c3v1 + 1/6.0*c3v2
        newsound[i] += ((c3*xfrac+c2)*xfrac+c1)*xfrac+c0
    return newsound

def optimal6_5z(infile, stepRatio):
    (fs, y) = UF.wavread(infile)
    lastI = len(y)/float(stepRatio)
    newsound = []
    for i in range(int(lastI+2)):
        newsound.append(0)
    newsound1 = np.float32(newsound)
    for i in range(1, int(lastI-3)):
        iTemp = stepRatio*i
        intItemp = int(iTemp)
        xfrac = iTemp - intItemp
        z = xfrac-0.5
        even1 = y[intItemp+1]+y[intItemp]
        odd1 = y[intItemp+1]-y[intItemp]
        even2 = y[intItemp+2]+y[intItemp-1]
        odd2 = y[intItemp+2]-y[intItemp-1]
        even3 = y[intItemp+3]+y[intItemp-2]
        odd3 = y[intItemp+3]-y[intItemp-2]
        c0 = even1*0.40513396007145713 + even2*0.09251794438424393 + even3*0.00234806603570670
        c1 = odd1*0.28342806338906690 + odd2*0.21703277024054901 + odd3*0.01309294748731515
        c2 = even1*-0.191337682540351941 + even2*0.16187844487943592 + even3*0.02946017143111912
        c3 = odd1*-0.16471626190554542 + odd2*-0.00154547203542499 + odd3*0.03399271444851909
        c4 = even1*0.03845798729588149 + even2*-0.05712936104242644 + even3*0.01866750929921070
        c5 = odd1*0.04317950185225609 + odd2*-0.01802814255926417 + odd3*0.00152170021558204
        newsound[i] += ((((c5*z+c4)*z+c3)*z+c2)*z+c1)*z+c0
    return newsound

def Hermite6_5z(infile, stepRatio):
    (fs, y) = UF.wavread(infile)
    lastI = len(y)/float(stepRatio)
    newsound = []
    for i in range(int(lastI+2)):
        newsound.append(0)
    newsound1 = np.float32(newsound)
    for i in range(1, int(lastI-3)):
        iTemp = stepRatio*i
        intItemp = int(iTemp)
        xfrac = iTemp - intItemp
        z = xfrac-0.5
        even1 = y[intItemp-2]+y[intItemp+3]
        odd1 = y[intItemp-2]-y[intItemp+3]
        even2 = y[intItemp-1]+y[intItemp+2]
        odd2 = y[intItemp-1]-y[intItemp+2]
        even3 = y[intItemp+0]+y[intItemp+1]
        odd3 = y[intItemp+0]-y[intItemp+1]
        c0 = 3/256.0*even1 - 25/256.0*even2 + 75/128.0*even3
        c1 = -3/128.0*odd1 + 61/384.0*odd2 - 87/64.0*odd3
        c2 = -5/96.0*even1 + 13/32.0*even2 - 17/48.0*even3
        c3 = 5/48.0*odd1 - 11/16.0*odd2 + 37/24.0*odd3
        c4 = 1/48.0*even1 - 1/16.0*even2 + 1/24.0*even3
        c5 = -1/24.0*odd1 + 5/24.0*odd2 - 5/12.0*odd3
        newsound[i] += ((((c5*z+c4)*z+c3)*z+c2)*z+c1)*z+c0
    return newsound

'''ynew = np.int16(y)
for i in y:
    print (y[i])'''
'''outfile = infile[:-4]+"linear_"+str(stepRatio)+".wav"
outfilea = infile[:-4]+"optimal6_5z_"+str(stepRatio)+".wav"
outfileb = infile[:-4]+"Bspline4_3_"+str(stepRatio)+".wav"
outfilec = infile[:-4]+"Hermite6_5z_"+str(stepRatio)+".wav"'''

'''newsound = linear()
print "linear:", outfile
newsounda = optimal6_5z()
print "optimal6_5z:", outfilea
newsoundb = Bspline4_3()
print "Bspline4_3:", outfileb
newsoundc = Hermite6_5z()
print "Hermite6_5z:", outfilec

newsound1 = np.float32(newsound)
newsounda1 = np.float32(newsounda)
newsoundb1 = np.float32(newsoundb)
newsoundc1 = np.float32(newsoundc)
print len(newsound)
print "greater than one:"
print "--------------------------"
UF.wavwrite(newsound1, 44100, outfile)
UF.wavwrite(newsounda1, 44100, outfilea)
UF.wavwrite(newsoundb1, 44100, outfileb)
UF.wavwrite(newsoundc1, 44100, outfilec)
print "Done..."'''
