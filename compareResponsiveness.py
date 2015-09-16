import os
import sys
from collections import defaultdict
import re
import math

class compareResponsiveness:

    def __init__(self, name, filename):
            self.name = name
            self.filename = filename


    def createResponsivenessDict(self) :
       
        resDict = defaultdict()
        assesorDict = defaultdict()
        myfile = open(self.filename, 'r')
        lines = myfile.readlines()
        myfile.close()

        lines = lines[7:]
        for l in lines :
            print(l)
            l = l.strip()
            xs = re.split('\s+', l)
            print(xs)
            if xs[0] not in assesorDict:
                assesorDict[xs[0]] = xs[2]
            
            if (xs[0],xs[3]) not in resDict:
                resDict[(xs[0],xs[3])] = xs[4]

        print(resDict)
        print(assesorDict)
        return (resDict, assesorDict)
                
    def findAvg(self, sysPerFile) :
    
         items = len(sysPerFile)
         sum = 0.00
         for v in sysPerFile.keys():
             sum += sysPerFile[v]
         return float(sum)/float(items)
             
    #def findBestnWorst(self, sysPerFile):



    def findVariance(self, sysPerFile):
    
        sumSq = 0.00
        items = len(sysPerFile) - 1
        avg = self.findAvg(sysPerFile)
        
        for k in sysPerFile.keys():
             sumSq += (sysPerFile[k] - avg)**2

        std_deviation = (sumSq / float(items) ) **0.5
        return std_deviation


    def findRange(self, sysPerFile):

         x = sorted(sysPerFile.items(), key =lambda x: x[1], reverse = True)
         print(x)
         best = x[0][1]
         worst = x[len(x)-1][1]
         print('Best:', best)
         print('Worst:', worst)
         rangeV = float(best - worst)/ 4.00
         bestScore = list()
         z = worst
         j = 1
         while j < 4 :
             z += rangeV
             bestScore.append(z)
             j += 1
         print(bestScore)
         bestScore = sorted(bestScore, reverse = True)
         print(bestScore)
         #input()
         return bestScore
    def findDistance(self, sysPerFile, p):
    
    
        x = sorted(sysPerFile.items(), key =lambda x: x[1], reverse = True)
        print(x)
        items = len(x)-1
        for i in range(0, (len(x)-1)):
            if x[i][0] == p:
                #sd = self.findVariance(sysPerFile)
                return i
        return -1
                
    def getResponseScore(self, resDict, assesorDict, sysPer, bestsysPer):
        countCorrect = 0
        countTotal = 0
        guessResponsivenessScore = defaultdict()
        
        for x in resDict:
            doc_id = x[0]
            peer_id = x[1]
            a = assesorDict[doc_id]
            val = resDict[x]
            key = (peer_id,a,doc_id)
            sysPerFile = defaultdict()
            
            for y in sysPer.keys():
                #print(y,'::',sysPer[y])
                if y[2] == doc_id and y[1] == a:
                   print(y, '>>', sysPer[y])
                   sysPerFile[y[0]] = sysPer[y][5]
            print(doc_id, '::', a, '::\n')
            if len(sysPerFile) == 0 :
                    continue
            '''
            rangeV = self.findRange(sysPerFile)
            # print guess responsiveness #
            indexV = 0
            myscore = 4
            if key in sysPer:
               while indexV < 3 :
                   if(sysPer[key][5] >= rangeV[indexV]) :
                       print(key, '>>',sysPer[key][5], '>>', myscore)
                       input()
                       break
                   else:
                       indexV += 1
                       myscore -= 1
            '''
            d = self.findDistance(sysPerFile, peer_id)
            if d == -1 :
                    continue
            d += 1
            totalSys = len(sysPerFile)
            position = float(totalSys - d) * 4.00 /float(totalSys)
            if key in sysPer:
                 performance = sysPer[key][5]
                 countTotal += 1
                 tfGuess = 'False'
                 #f.write(doc_id +' >> '+ a + ' >> '+ peer_id + ' >> '+ val+' >> '+ str(position))
                 if math.fabs(float(val) - position) <= 0.5 :
                     countCorrect += 1
                     #f.write(' >> True\n')
                     tfGuess = 'True'
                     #else:
                     #f.write(' >> False\n')
                 guessResponsivenessScore[(doc_id,a,peer_id)] = (val, position, tfGuess)
             #z = input()
        print(len(guessResponsivenessScore))
        myKeys = guessResponsivenessScore.keys()
        myKeyList = sorted(myKeys, key = lambda x: x[0])
        f=open("responsivenessGuess05.txt","w")
        f.write('(Doc, Assessor, Peer) >> (Responsiveness, i-measure-Guess, True/False)\n')

        print(myKeyList)
        for k in myKeyList:
            f.write(str(k[0])+', '+ str(k[1])+', '+ str(k[2]) + '>> ')
            (r,i,t) = guessResponsivenessScore[k]
            f.write('(' + str(r)+ ', '+ str(i) + ', '+ str(t) +')\n')
        f.write('\nCorrect: '+str(countCorrect)+ 'out of '+str(countTotal))

        f.close()





