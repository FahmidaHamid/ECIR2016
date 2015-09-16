import os
import sys
import re
import string
from collections import defaultdict

class determineNKL:

    def __init__(self, name):
        self.name = name

    def observeIntersection(self, set1, set2):

        return set1.intersection(set2)
    
    
    def generatePairs(self, set1) :
    
        allPairs = set()
    
        for x in set1 :
            for y in set1:
                if x != y :
                   allPairs.add((x,y))
                   allPairs.add((y,x))
        return allPairs

    

    def countnkl(self, set1, set2, set3) :

        n = len(set1)
        k = len(set2)
        l = len(set3)
        overlappedSet = self.observeIntersection(set2,set3)
        #print(set1)
        #print(set2)
        #print(set3)
        #print(overlappedSet)
        z = len(overlappedSet)
        ravg = float(k * l)/ float(n)
        if ravg != 0 :
          imeasure = float(z)/ravg
        else:
            imeasure = -1 #not comparable
        #print(z,'::',imeasure)
        #x = input()
        return (n,k,l,z,ravg,imeasure)

    def createNKLDictionary(self, dataDictionary, humanids, systemids, hsummaries, ssummaries, fileids):


        systemPerformance = defaultdict()
        for f in fileids :
            #print('File Name:', f)
            fileData = dataDictionary[f]
            for h in humanids :
                if (h,f) in hsummaries.keys() :
                         #print('Participating Human: ', h)
                         humanSummaryData = hsummaries[(h,f)]
                         for s in systemids :
                             if (s,f) in ssummaries:
                               #print('Participating System:', s)
                               systemSummaryData = ssummaries[(s,f)]
                               (n,k,l,z,ravg,imeasure) = self.countnkl(fileData, humanSummaryData,systemSummaryData)
                               systemPerformance[(s,h,f)] = (n,k,l,z,ravg,imeasure)


        return systemPerformance
    
    def findNeighbors(self,h,f,hids) :
        neighborListh = set()
        for h1 in hids.keys():
            if h1 != h  and f in hids[h1]:
                neighborListh.add(h1)
        
        return neighborListh
    

    def createGoldNKLDictionary(self, dataDictionary, hids,hsummaries,fileids):

        goldPerformance = defaultdict()

        for h in hids.keys() :
            for h1 in hids.keys():
                if h != h1 :
                    for f in hids[h]:
                      if f in hids[h1]:
                        if (h,h1,f) not in goldPerformance and (h1,h,f) not in goldPerformance :
                            goldSummaryK = hsummaries[(h,f)]
                            goldSummaryL = hsummaries[(h1,f)]
                            fileData = dataDictionary[f]
                            (n,k,l,z,ravg,imeasure) = self.countnkl(fileData,goldSummaryK,goldSummaryL)
                            goldPerformance[(h,h1,f)] = (n,k,l,z,ravg,imeasure)
                            goldPerformance[(h1,h,f)] = (n,l,k,z,ravg,imeasure)


        return goldPerformance


    def normalizeGoldPerformance(self, fileids, hids, goldPerformance):
    
       normalizedGoldPerformance = defaultdict()
       bestf = defaultdict()

       fileK= set()
        
       for h in hids:
            files = hids[h]
            for f in files:
                if f not in fileK :
                    neighbors_h = self.findNeighbors(h,f,hids)
                    participants = neighbors_h.union(set([h]))
                    fileK.add(f)
                    edge_pairs = self.generatePairs(participants)
                    best = 0.00 
                    for e in edge_pairs:
                        if best < goldPerformance[(e[0],e[1],f)][5]  :
                                  best = goldPerformance[(e[0],e[1],f)][5]
                    bestf[f] = best
                    for e in edge_pairs:
                           if best != 0.00:
                                normalizedGoldPerformance[(e[0],e[1],f)] = goldPerformance[(e[0],e[1],f)][5]/best
                              
                           else:
                               normalizedGoldPerformance[(e[0],e[1],f)] = 0.00
                                       
       return (bestf, normalizedGoldPerformance)




    def normalizeSystemPerformance(self, fileids, hids, sids, systemPerformance) :

        bestPerformance = defaultdict()
        normalizedSysPerformance = defaultdict()
        
        for f in fileids:
            for h in hids:
              if f in hids[h]:
                for s in sids:
                  if f in sids[s]:
                     neighbors_s = self.findNeighbors(s,f,sids)
                     participants = neighbors_s.union(set([s]))
                     bestp = 0.00
                     winnerSystem = set()
                     for p in participants :
                        if systemPerformance[(p,h,f)][5] >= bestp :
                              if systemPerformance[(p,h,f)][5] == bestp :
                                    winnerSystem.add(p)
                              else:    
                                    bestp = systemPerformance[(p,h,f)][5]
                                    winnerSystem = set([p]) 
                     bestPerformance[(f,h)] = (bestp, set(winnerSystem))
                     for n in participants :     
                        normalizedSysPerformance[(n,h,f)] = systemPerformance[(n,h,f)][5]/bestPerformance[(f,h)][0]

        return (bestPerformance, normalizedSysPerformance)



    def countNeighborships(self, hids) :

            neighborSet = defaultdict()
            for h in hids :
                file_h = hids[h]
                for h1 in hids:
                    file_h1 = hids[h1]
                    if h != h1 :
                         common = file_h.intersection(file_h1)
                         neighborSet[(h,h1)] = common
                         neighborSet[(h1,h)] = common


            for tuple in neighborSet:
                print('Tuple: ', tuple, '>>', neighborSet[tuple])
            print('Total Tuples: ', len(neighborSet))



      
    def countSystemBetterthanHuman(self, bestPerformance):

        count = 0
        for (f, h) in bestPerformance.keys():
                bestSystems = bestPerformance[(f,h)][1]
                length_bs = len(bestSystems)
                if length_bs == 1 and h not in bestSystems :
                    print(f,':',h,':', bestSystems)
                    count += 1
                elif length_bs > 1 :
                    print(f,':',h,':', bestSystems)
                    count += 1
                else:
                    continue
              
 
        return count
     

    def comparePerformancePair(self, nPerformance, hids, fileids) :

        pairedPerformance = defaultdict()
        pairCount = defaultdict()
        fileK = set()
        
        for h in hids :
            print(h)
            f = set(hids[h])
            print('Files: ', f)
            for fz in f:
                if fz not in fileK:
                   neighbors_h = self.findNeighbors(h,fz,hids)
                   print('Neighbors of h = ', neighbors_h)
                   participants = neighbors_h.union(set([h]))
                   print('Participants in file f', participants)
                   fileK.add(fz)
                   edge_pairs = self.generatePairs(participants)
                   print('Edge Pairs: ', edge_pairs)
                   for e in edge_pairs:
                       if (e[0],e[1]) in pairedPerformance :
                            pairedPerformance[(e[0],e[1])] += nPerformance[(e[0],e[1],fz)]
                            pairCount[(e[0],e[1])] += 1
                       else:
                            pairedPerformance[(e[0],e[1])] = nPerformance[(e[0],e[1],fz)]
                            pairCount[(e[0],e[1])] = 1


        print('\nPair, Performance\n')
        for e in pairedPerformance :
              pairedPerformance[e] = float(pairedPerformance[e])/float(pairCount[e])
              print(e, pairedPerformance[e])
              #x = input()

        return pairedPerformance












