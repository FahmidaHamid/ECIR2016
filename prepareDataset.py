import os
import sys
import re
import string
from collections import defaultdict
from nltk.stem.porter import *
from nltk.corpus import  stopwords



class prepareDataset :
    
    estopwords = set(stopwords.words('english'))
    stemmer = PorterStemmer()

    def __init__(self, name) :
         self.name = name
    
    
    def cleanhtml(self, raw_html):
    
         cleanr =re.compile('<.*?>')
         cleantext = re.sub(cleanr,'', raw_html)
         return cleantext


    def cleanRawText(self, rawText):
         cleanText = self.cleanhtml(rawText)
         cleanText = '\n'.join(cleanText.split('\n')[4:])
         cleanText = re.sub(r'[^\x00-\x7f]',r' ',cleanText)
         cleanText.rstrip()
         cleanText = cleanText.replace('\'\'', '\"').replace('``','\"').replace('\t', ' ')
         cleanText = cleanText.replace('\"', ',').replace('!\"', ',').replace('.\"', ',').replace('(', ' ').replace(')', ' ')
         cleanText = cleanText.replace('\n', ',').replace('=',',').replace('+',',').replace('-', ' ').replace('#', ' ').replace('?', ' ').replace('!', ' ')
         pattern2 = re.compile('[ |, |; |.|-|(|)]+')
         pattern3 = re.compile('[\'|\"|:]+')
         cleanText = re.sub(pattern2, ',', cleanText)
         cleanText = re.sub(pattern3,' ',cleanText)
         words = re.split(',', cleanText)
         wordSet = set(words)
         wordSet = wordSet.difference(['']) 
         return wordSet

    

    def readDocuments(self, path) :

        dataDictoinary = defaultdict(set)

        for dirN, subDirN, fileL in os.walk(path) :
            if dirN == '.DS_Store' :
               print ('Ignore')
            else :
               #print "Found Directory: " + dirN
               for fname in fileL :
                  if fname != '.DS_Store' :
                      reader = open(dirN + '/'+ fname, 'r')
                      wordSet =  self.cleanRawText(reader.read().lower())
                      wordSet = wordSet.difference(self.estopwords)
                      #print(wordSet)
                      
                      folderName = dirN.rsplit('/', 1)[1].upper()
                      fileName = folderName.replace('T','') + '.'+fname.replace('.txt','')

                      for w in wordSet :
                           ws = self.stemmer.stem(w)
                           if ws and len(ws) > 1 :
                               dataDictoinary[fileName].add(ws)

                      print(fileName, dataDictoinary[fileName])
                      #x = input()

        return dataDictoinary

    '''
    def clusterDocuments(self, dataDictionary) :


        clusterDictionary = defaultdict()
        updated = defaultdict()
        for f, wSet in dataDictionary.items():
               clusterName = f.split('.')[0]
               clusterName = clusterName[:-1]
               print(f, '>> comes from >> ', clusterName)
               print(wSet)
               if clusterName in clusterDictionary.keys() :
                    clusterDictionary[clusterName] = clusterDictionary[clusterName].union(wSet)
                    updated[clusterName] += 1
               else:
                    clusterDictionary[clusterName] = wSet
                    updated[clusterName] = 1
               print(clusterDictionary[clusterName])
               print(len(clusterDictionary[clusterName]))   
               x = input()
        for c, wSet in clusterDictionary.items():
             print(c)
             print(wSet)
             print('Total Words: ', len(wSet))
             print('Updated: ', updated[c], ' times')
             

               
        return clusterDictionary

    '''


          


 



    

