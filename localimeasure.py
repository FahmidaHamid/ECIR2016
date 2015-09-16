import sys
import os
from collections import defaultdict

class localimeasure:

    def __init__(self, name):
        self.name = name
  
    def credibilityH(self, f, h, neighborListh, gperformanceSet) : #credibility is determined per file
        c_h = 0.00
        for n in neighborListh :
            if (h,n,f) in gperformanceSet :
               c_h += gperformanceSet[(h,n,f)][5]# 6th  item in the tuple is the imeasure
            else:
               c_h += gperformanceSet[(n,h,f)][5]
        c_h = float(c_h)/ float(len(neighborListh))
        return c_h


    def findNeighbors(self,h,f,hids) :
         neighborListh = set()

         for h1 in hids.keys():
             if h1 != h  and f in hids[h1]:
                    neighborListh.add(h1)

         return neighborListh

    def defineCredibilityDict(self, fileids, hids, goldPerformance):

        credibilityDict = defaultdict()
        
        for h in hids.keys() :
              fileList = hids[h]
              for f in fileList:
                  neighborListh = self.findNeighbors(h,f,hids)
                  credibilityDict[(h,f)] = self.credibilityH(f,h,neighborListh,goldPerformance)


        return credibilityDict



    def scoreS(self, f, s, neighborList, sperformanceSet, credibilityDict):
        score_s = 0.00

        for n in neighborList :
            score_s += credibilityDict[(n,f)] * sperformanceSet[(s,n,f)][5]
        iscore_s = float(score_s) / float(len(neighborList))
        return iscore_s

    def nscoreS(self, f, s, neighborList, snperformanceSet, ncredibilityDict):
        score_s = 0.00
        for n in neighborList :
            score_s += ncredibilityDict[(n,f)] * snperformanceSet[(s,n,f)]
        iscore_s = float(score_s) / float(len(neighborList))
        return iscore_s



    def localiscore(self, sids, hids, systemPerformance, credibilityDict) :
        
        iscoreLocal = defaultdict()
        iscore = defaultdict()
        for s in sids.keys() :
            fileList = sids[s]
            iscoreAvg = 0.00
            for f in fileList :
               sneighbors = self.findNeighbors(s,f,hids)
               iscores = self.scoreS(f,s,sneighbors,systemPerformance,credibilityDict)
               iscoreLocal[(s,f)] = iscores
               iscoreAvg += iscores
            iscore[s] = float(iscoreAvg)/ float(len(fileList))

        return (iscore, iscoreLocal)
    
    
    def ncredibilityH(self, f, h, neighborListh, normalizedGoldPer) : #credibility is determined per file
        c_h = 0.00
        for n in neighborListh :
            if (h,n,f) in normalizedGoldPer :
                c_h += normalizedGoldPer[(h,n,f)]
        c_h = float(c_h)/ float(len(neighborListh))
        return c_h


    def definenormCredibilityDict(self, fileids, hids, normalizedGoldPer) :


        normcredibilityDict = defaultdict()
    
        for h in hids.keys() :
            fileList = hids[h]
            for f in fileList:
                     neighborListh = self.findNeighbors(h,f,hids)
                     normcredibilityDict[(h,f)] = self.ncredibilityH(f,h,neighborListh,normalizedGoldPer)
        
        return normcredibilityDict


    def normlocaliscore(self, sids, hids, normalizedSysPer, localCredibility1) :

        iscoreLocal = defaultdict()
        iscore = defaultdict()
        for s in sids.keys() :
             fileList = sids[s]
             iscoreAvg = 0.00
             for f in fileList :
                 sneighbors = self.findNeighbors(s,f,hids)
                 iscores = self.nscoreS(f,s,sneighbors,normalizedSysPer,localCredibility1)
                 iscoreLocal[(s,f)] = iscores
                 iscoreAvg += iscores
             iscore[s] = float(iscoreAvg)/ float(len(fileList))
    
        return (iscore, iscoreLocal)









