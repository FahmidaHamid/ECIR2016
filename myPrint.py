import os
import sys


class myPrint:
   dirname = ''
   def __init__(self, name, dirname) :
       self.name = name
       self.dirname = dirname

   def printhids(self, fname, hids) :
       fileName = self.dirname + '/'+ self.name + '.'+fname + '.txt'
       myF = open(fileName, 'w')
       nameList = list(hids.keys())
       names = ', '.join(str(x) for x in nameList)
       myF.write('Participant Ids: '+ names + '\n')
       for h in hids.keys() :
           myF.write(h)
           myF.write('\n')
           myF.write('>> Total: ' + str(len(hids[h]))+ 'Files\n')
           x = list(hids[h])
           myStr = ', '.join(str(e) for e in x)
           myF.write(myStr)
           myF.write('\n')
       myF.close()

   def printSystemPerformance(self, fileids, sids, hids, sysPerformance, nSysPerformance ) :
        fileName = self.dirname + '/'+ self.name + 'SystemPerformance.txt'
        myF = open(fileName, 'w')
        myF.write('(Filename, Human1, Human2) = (n,k,l,observed_overlap, baseline, i-measure, normalized_i-measure))\n')
        for f in fileids:
          for s in sids.keys() :
              for h in hids.keys() :
                  if (f in sids[s]) and (f in hids[h]) :
                     myF.write(str(f)+ ', '+str(s)+', '+str(h)+') = ')
                     (n,k,l,z,random, imeasure) = (sysPerformance[(s,h,f)])
                     n_imeasure = nSysPerformance[(s,h,f)]    
                     myF.write('('+str(n)+', '+str(k)+', '+str(l)+', '+str(z)+ ', '+ str(random) +', '+ str(imeasure)+', '+ str(n_imeasure)+')\n')
        myF.close()



   def printGoldPerformance(self, fileids, hids, goldPerformance, ngoldPer ) :
       
       fileName = self.dirname + '/'+ self.name + 'GoldPerformance.txt'
       myF = open(fileName, 'w')
       myF.write('(Filename, System, Human) = (n,k,l,observed_overlap, baseline, i-measure, normalized_i-measure))\n')
       (n,k,l,z,random, imeasure) = (0,0,0,0,0,0)
       for f in fileids :
           for s in hids.keys() :
               for h in hids.keys() :
                   if h != s:
                       if (f in hids[s]) and (f in hids[h]) :
                          
                           (n,k,l,z,random, imeasure) = goldPerformance[(s,h,f)]
                           n_imeasure = ngoldPer[(s,h,f)] 
                           myF.write('('+str(f)+ ', '+str(s)+', '+str(h)+') = ')
                           myF.write('('+str(n)+', '+str(k)+', '+str(l)+', '+str(z)+ ', '+ str(random) +', '+ str(imeasure)+', '+ str(n_imeasure)+')\n')
                       else :
                            continue
       myF.close()

   def printLocalCredibility(self, fileids,hids, localCredibility,val) :
           fileName = self.dirname + '/'+ self.name + val+ '_CredibilityScore.txt'
           myF = open(fileName, 'w')
           myF.write('(Filename, Human, Credibility_Score)\n')

           for f in fileids :
               for h in hids :
                   if f in hids[h] :
                       lcredibility = localCredibility[(h,f)]
                       myF.write(str(f) + ', '+str(h)+ ', '+ str(lcredibility)+'\n')
           myF.close()
           return

   def printGlobalCredibility(self,hSet, localCredibility, val) :
           fileName = self.dirname + '/'+ self.name+ str(val) + '_GlobalCredibilityScore.txt'
           myF = open(fileName, 'w')
           myF.write('(Human, Credibility_Score)\n')
           d1 = sorted(localCredibility.items(), key = lambda x: x[1], reverse= True)
           for x in d1 :
                       #lcredibility = x[1]
                       myF.write(str(x[0])+ ', '+ str(x[1])+'\n')
           myF.close()
           return
   def printPairedPerformance(self, pairedPerformance):
       fileName = self.dirname + '/'+ self.name + '_LocalPairScore.txt'
       myF = open(fileName, 'w')
       myF.write('Human_Pair, PairedPerformance\n')

       d2 = sorted(pairedPerformance.items(), key = lambda x: x[1], reverse = True)
       for (x,y) in d2 :
            myF.write(str(x)+ ', '+ str(y)+'\n')
       myF.close()
       return




   def printFinalScore(self, finalScore,val) :

    fileName = self.dirname + '/'+ self.name + 'FinalScore'+'_'+val+'.txt'
    myF = open(fileName, 'w')
    myF.write('(Name >> iScore)\n')
    
    fscore = sorted(finalScore.items(), key=lambda x: x[1], reverse = True)
    for item in fscore :
        myF.write(str(item[0])+'>>'+ str(item[1])+ '\n')
    myF.close()
    return

   def printLocalScoreperFile(self, finalScoreperFile,val) :
    
    
       d2 = {}

       for (w,u) , value in finalScoreperFile.items():
         if u not in d2:
            d2[u] = [(w,value)]
         else:
           d2[u].append((w, value))

    
       fileName = self.dirname + '/'+ self.name + 'FinalScoreperFile'+'_'+val+'.txt'
       myF = open(fileName, 'w')
       myF.write('(>>File >> Name >> iScore)\n')
    
       for key, values in d2.items():
           myF.write(str(key) + ':\n')
           myVals = sorted(values, key=lambda x:x[1], reverse = True)
           for x in myVals:
               myF.write(':\t'+str(x[0])+'>>'+str(x[1])+'\n')


       myF.close()
       return




   def printBestScore(self,bestPer, fileids, hids):

       print('Best Performances per File/Human')
       for f in fileids:
         for h in hids :
             if f in hids[h]:
                 if (f,h) in bestPer :
                     print(f, '::', h,'::',bestPer[(f,h)])
       return

   def printnormalizedGoldPer(self, fileids, hids, nomalizedGoldPer):
       for f in fileids:
           for h in hids :
               if f in hids[h]:
                   for h1 in hids:
                       if h != h1 :
                          if (h, h1,f) in nomalizedGoldPer :
                               print(f, '::', h,'::', h1,'::',nomalizedGoldPer[(h,h1,f)])
       return









