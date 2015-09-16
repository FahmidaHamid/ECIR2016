import os
import sys
import re
from collections import defaultdict
from nltk.stem.porter import *
from nltk.corpus import  stopwords

class readMTestSummaries :
      estopwords = set(stopwords.words('english'))
      stemmer = PorterStemmer()

      def __init__(self, name):
          self.name = name


      def extractSingleSummaryFileInfo(self,fname, sample) :
          
            fwordSet = set()

            pattern2 = re.compile('[ |, |; |\-|(|)|\|/|=|]+')
            pattern3 = re.compile('[_|\'|\"|:|!|?|\`]+')
            pattern4 = re.compile('.')
            fs = fname.split('.')
            clusterID = fs[0]
            hid = fs[4]
            if fs[1] == 'M' :
                 for sen in sample :
                     sen = sen.lower()
                     sen = sen.rstrip('\n')
                     if sen.endswith('.'):
                        sen = re.sub('\.$', ' .', sen)
                     x = re.sub(pattern2, ',', sen)
                     x = re.sub(pattern3,',',x)
                     words = re.split(',', x)
                     wordSet = set(words)
                     wordSet = wordSet.difference(self.estopwords)
                     wordSet = wordSet.difference(set(['']))
                     for w in wordSet:
                          w = w.lstrip(' ')
                          w = w.rstrip(' ')
                          z = self.stemmer.stem(w).lower()
                          z = z.rstrip('.')
                          if len(z) > 1 :
                             fwordSet.add(z)
                     #print(words)
                     #print(fwordSet)
                 #print(fwordSet)
                 #x = input()
                 return (clusterID, hid, fwordSet, 0) # human written single-doc summary found
    
            return ('','0', set(), 1)
        
        
      def readSummaries(self, testDir):
            #humanDir = '/Users/fahmida/Desktop/AAAIimeasure/data/dataSetHuman'
            
            testSummaries = defaultdict()
            ids = defaultdict()
            fileIds = defaultdict()
            
            for root, dirs, files in os.walk(testDir, topdown=False):
                count = 0
                for name in files:
                    #print(name)
                    if not name.startswith('.') :
                        absPath = os.path.join(root,name)
                        myF = open(absPath, "r",encoding='utf-8', errors='ignore')
                        lines = myF.readlines()
                        myF.close()
                        #print(lines)
                        if len(lines) > 0 :
                            (fname, hid, fwordSet, errorCode)= self.extractSingleSummaryFileInfo(name, lines)
                            if errorCode != 1 :
                                testSummaries[(hid, fname)] = fwordSet
                                if hid in ids:
                                    ids[hid].add(fname)
                                else :
                                    ids[hid] = set([fname])
                                
                                if fname in fileIds:
                                    fileIds[fname].add(hid)
                                else :
                                    fileIds[fname] = set([hid])
                            count += 1
            #print('Total Files: ', count)
            
            
            for h1 in ids.keys() :
                for k, v in testSummaries.items() :
                    if k[0] == h1 :
                        print (k, v)
            
            return (ids, fileIds, testSummaries)

