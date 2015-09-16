import os
import sys
import re
from collections import defaultdict
from nltk.stem.porter import *
from nltk.corpus import  stopwords

#from operator import itemgetter
#import itertools

class readTestSummaries:
  estopwords = set(stopwords.words('english'))
  stemmer = PorterStemmer()
  
  def __init__(self, name) :
          self.name = name


  def cleanhtml(self, rawHtml) :
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr,'',rawHtml)
    return cleantext


  def extractSingleSummaryFileInfo(self,sample) :
        pattern = re.compile('^\[\d+\]')
        pattern2 = re.compile('[ |, |; |\-|(|)]+')
        pattern3 = re.compile('[\'|\"|:|!|?\`]+')
        pattern4 = re.compile('.')  
       
        f2 = sample[0].split('.')
        global estopwords
        extraStopwords = set(['of', 'in','by', 'off', 'the', 'at', 'a','an','and','or','nor','neither','either'])
        if f2[1] == 'P' :
            fname = f2[0].upper()+'.'+f2[5].upper()+ '.'+f2[6]
            hid = f2[4].upper()
            print(fname)
            sample.pop(0) #remove the first item
            for sen in sample :
                   sen = sen.lower()
                   #print(sen)
                   if sen.endswith('.'):
                         sen = re.sub('\.$', ' .', sen)
                         #print(sen)
                         
                   x = re.sub(pattern, '', sen)
                   x = re.sub(pattern2, ',', x)
                   x = re.sub(pattern3,' ',x)
                   words = re.split(',', x)
                   words.remove('')
                   wordSet = set(words)
                   wordSet = wordSet.difference(self.estopwords)
                   wordSet = wordSet.difference(extraStopwords)
                   fwordSet = set()
                   for w in wordSet:
                       w = w.lstrip(' ')
                       w = w.rstrip(' ')
                       z = self.stemmer.stem(w).lower()
                       z = z.rstrip('.')
                       if len(z) > 1 :
                          fwordSet.add(z)
                   #print(words)
                   #print(fwordSet)
            print(fwordSet)
            #x = input()
            return (fname, hid, fwordSet, 0) # human written single-doc summary found
 
        return ('','0', set(), 1)


  def readSummaries(self, humanDir):
        #humanDir = '/Users/fahmida/Desktop/AAAIimeasure/data/dataSetHuman'

        humanSummaries = defaultdict()
        humanIds = defaultdict()
        fileIds = defaultdict()

        for root, dirs, files in os.walk(humanDir, topdown=False):
            count = 0
            for name in files:
                #print(name)
                if not name.startswith('.') :
                   absPath = os.path.join(root,name)
                   myF = open(absPath, "r",encoding='utf-8', errors='ignore')
                   lines = myF.readlines()
                   myF.close()
                   #print(lines)
                   fileData = []
                   for l in lines :
                       cleanline = self.cleanhtml(l.rstrip())
                       if cleanline:
                          fileData.append(cleanline)
                   if len(fileData) > 0 :
                      (fname, hid, fwordSet, errorCode)= self.extractSingleSummaryFileInfo(fileData)
                      if errorCode != 1 :
                         humanSummaries[(hid, fname)] = fwordSet
                         if hid in humanIds:
                              humanIds[hid].add(fname)
                         else :
                              humanIds[hid] = set([fname])
                     
                         if fname in fileIds:
                              fileIds[fname].add(hid)
                         else :
                              fileIds[fname] = set([hid])
                      count += 1
        print('Total Files: ', count)


        for h1 in humanIds.keys() :
            for k, v in humanSummaries.items() :
               if k[0] == h1 :
                  print (k, v)

        return (humanIds, fileIds, humanSummaries)
