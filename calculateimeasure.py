from readTestSummaries import readTestSummaries
from readMTestSummaries import readMTestSummaries
from prepareDataset import prepareDataset
from prepareMDataset import prepareMDataset
from determineNKL import determineNKL
from localimeasure import localimeasure
from globalimeasure import globalimeasure
from myPrint import myPrint
from compareResponsiveness import compareResponsiveness
import os


####################
# Common abvs.     #
# d = data         #
# h = human     ####
# s = system     ###
# p,q = print obj  #
# n = normalized   #
# m = multi-doc    #
# u = un_normalized#
# g = global       #
# l = local        #
####################



#########################################################################
###################         Input File Paths        #####################
#########################################################################

hpath = '/Users/fahmida/Desktop/AAAIimeasure/data/dataSetHuman'
spath = '/Users/fahmida/Desktop/AAAIimeasure/data/dataSetSystem'
dpath = '/Users/fahmida/Desktop/AAAIimeasure/data/dataSetDUC2004'
mdpath = '/Users/fahmida/Desktop/AAAIimeasure/data/DUC2004_Summarization_Documents/duc2004_testdata/task5/duc2004_task5_docs/docs'
mhpath = '/Users/fahmida/Desktop/AAAIimeasure/data/duc2004_results/ROUGE/task5/models'
mspath = '/Users/fahmida/Desktop/AAAIimeasure/data/duc2004_results/ROUGE/task5/peers'
responsivePath = '/Users/fahmida/Desktop/AAAIimeasure/data/duc2004_results/Responsiveness/results.table.R'
#########################################################################
###############          Dir to write outputs        ####################
#########################################################################

outDir = 'outputLocalIScore'
currentDir = os.getcwd()
outPath = currentDir + '/'+outDir
os.makedirs(outPath, exist_ok=True)

goutDir = 'outputGlobalIScore'
goutPath = currentDir + '/'+goutDir
os.makedirs(goutPath, exist_ok = True)

moutDir = 'outputLocalIScoreMulti'
moutPath = currentDir + '/'+moutDir
os.makedirs(moutPath, exist_ok=True)

mgoutDir = 'outputGlobalIScoreMulti'
mgoutPath = currentDir + '/'+mgoutDir
os.makedirs(mgoutPath, exist_ok=True)


############################################################################
###################              Print Object        #######################
############################################################################
p = myPrint('Local Results', outPath) #single-doc summary-local approach
q = myPrint('Global Results', goutPath) #single-doc summary-global approach
mp = myPrint('Local Results Task5', moutPath)#multi-doc summary-local approach
mq = myPrint('Global Results Task5', mgoutPath)#multi-doc summary-global approach

############################################################################
############  Single Document Summary Evaluation        ####################
############################################################################
hs = readTestSummaries('DUC2004_Task1')
(hids, fileids, hsummaries) = hs.readSummaries(hpath)

ss = readTestSummaries('DUC2004_Task1')
(sids, sfileids, ssummaries) = ss.readSummaries(spath)

ds = prepareDataset('DUC2004_Task1')
dataDictionary = ds.readDocuments(dpath)

cresponse = compareResponsiveness('DUC2004_Task5', responsivePath)
(responseDict, assessorDict) = cresponse.createResponsivenessDict()


##################################################################################################
##### nkl object has the methods to calculate n,k,l,rand_avg,i-measure, normalized i-measure #####
##################################################################################################
nkl = determineNKL('DUC2004_Task1')
sysPerformance = nkl.createNKLDictionary(dataDictionary, hids, sids, hsummaries, ssummaries, fileids)
(bestSysPer, normalizedSysPer) = nkl.normalizeSystemPerformance(fileids, hids, sids, sysPerformance)

goldPerformance = nkl.createGoldNKLDictionary(dataDictionary, hids,hsummaries,fileids)
(bestGolPer, normalizedGoldPer) = nkl.normalizeGoldPerformance(fileids, hids, goldPerformance)
pairedPerformance = nkl.comparePerformancePair(normalizedGoldPer,hids,fileids)
##################################################################################################
###### lm: (local approach) object has the methods to define credibility             #############
###### of the humans and calculate the i-scores for each systems                       ###########
##################################################################################################

lm = localimeasure('DUC2004Local')
ulocalCredibility = lm.defineCredibilityDict(fileids, hids, goldPerformance)
(ulfinalScore, ulocalScoreperFile) = lm.localiscore(sids, hids, sysPerformance, ulocalCredibility)

nlocalCredibility = lm.definenormCredibilityDict(fileids, hids, normalizedGoldPer)
(nlfinalScore, nlocalScoreperFile) = lm.normlocaliscore(sids, hids, normalizedSysPer, nlocalCredibility)


##################################################################################################
###### gm: (global approach) object has the methods to define credibility             ############
###### of the humans and calculate the i-scores for each systems                       ###########
##################################################################################################

gm  = globalimeasure('DUC2004Global')
ugraph = gm.defineGraph(fileids,hids,goldPerformance,5)
(ugraph, globalCredibility) = gm.rankCredibility(ugraph)
gm.printRank(ugraph)
ugFinalScore = gm.globaliscore(sids,hids,sysPerformance,globalCredibility, 5)

ngraph = gm.defineGraph(fileids,hids,normalizedGoldPer,-1)
(ngraph, nglobalCredibility) = gm.rankCredibility(ngraph)
#gm.printRank(ngraph)
ngFinalScore = gm.globaliscore(sids,hids,normalizedSysPer, nglobalCredibility, -1)

###################################################################
######  Print Results to specified Folder             #############
###################################################################
p.printhids('Human', hids)
p.printhids('System', sids)

p.printSystemPerformance(fileids, sids, hids, sysPerformance,normalizedSysPer)
p.printGoldPerformance(fileids, hids, goldPerformance,normalizedGoldPer)
#p.printBestScore(bestSysPer, fileids, hids)
#c = nkl.countSystemBetterthanHuman(bestSysPer)
#print('Total: ', c, ' cases Systems perform as good as Humans')
p.printFinalScore(ulfinalScore, 'un_normalized')
p.printFinalScore(nlfinalScore,'normalized')
p.printLocalCredibility(fileids,hids, ulocalCredibility, 'un_normalized')
p.printLocalCredibility(fileids,hids, nlocalCredibility, 'normalized')
p.printPairedPerformance(pairedPerformance)
p.printLocalScoreperFile(nlocalScoreperFile, 'normalized')
q.printFinalScore(ugFinalScore, 'Global')
q.printFinalScore(ngFinalScore, 'Normalized_Global')
q.printGlobalCredibility(hids.keys(), globalCredibility, 'un_normalized')
q.printGlobalCredibility(hids.keys(), nglobalCredibility, 'normalized')
##################################################################################

############################################################################
#############  Multi-Document Summary Evaluation        ####################
############################################################################

mds = prepareMDataset('DUC2004_Task5')
mdataDic = mds.readDocuments(mdpath)
mdataDictionary = mds.clusterDocuments(mdataDic)

mhs = readMTestSummaries('DUC2004_Task5')
(mhids, mfileids, mhsummaries) = mhs.readSummaries(mhpath)

mss = readMTestSummaries('DUC2004_Task5')
(msids, msfileids, mssummaries) = mss.readSummaries(mspath)



#just to check the results
print(msids.keys())
print(mhids.keys())
print(mfileids.keys())
print(mdataDictionary.keys())
print(len(mfileids.keys()), '>>', len(mdataDictionary.keys()))

nkl5 = determineNKL('DUC2004_Task5')
msysPerformance = nkl5.createNKLDictionary(mdataDictionary, mhids, msids, mhsummaries, mssummaries, mfileids)
(mbestSysPer, mnormalizedSysPer) = nkl5.normalizeSystemPerformance(mfileids, mhids, msids, msysPerformance)

cresponse.getResponseScore(responseDict, assessorDict, msysPerformance, mbestSysPer)



mgoldPerformance = nkl5.createGoldNKLDictionary(mdataDictionary, mhids,mhsummaries,mfileids)
(mbestGolPer, mnormalizedGoldPer) = nkl5.normalizeGoldPerformance(mfileids, mhids, mgoldPerformance)

lm5 = localimeasure('DUC2004Local_Task5')
ulocalCredibility5 = lm5.defineCredibilityDict(mfileids, mhids, mgoldPerformance)
(ulfinalScore5, ufinalScoreperFile5)= lm5.localiscore(msids, mhids, msysPerformance, ulocalCredibility5)


nlocalCredibility5 = lm5.definenormCredibilityDict(mfileids, mhids, mnormalizedGoldPer)
(nlfinalScore5, nfinalScoreperFile) = lm5.normlocaliscore(msids, mhids, mnormalizedSysPer, nlocalCredibility5)

mp.printFinalScore(ulfinalScore5, 'un_normalized')
mp.printFinalScore(nlfinalScore5,'normalized')
mp.printLocalCredibility(mfileids,mhids, ulocalCredibility5, 'un_normalized')
mp.printLocalCredibility(mfileids,mhids, nlocalCredibility5, 'normalized')
mp.printBestScore(mbestSysPer, mfileids, mhids)
#c5 = nkl5.countSystemBetterthanHuman(mbestSysPer)
#print('Total: ', c5, ' cases Systems perform as good as Humans')


gmm  = globalimeasure('DUC2004Global_Task5')
mugraph = gmm.defineGraph(mfileids,mhids,mgoldPerformance,5)
(mugraph, mglobalCredibility) = gmm.rankCredibility(mugraph)
gmm.printRank(mugraph)
mugFinalScore =gmm.globaliscore(msids,mhids,msysPerformance,mglobalCredibility, 5)

mngraph = gmm.defineGraph(mfileids,mhids,mnormalizedGoldPer,-1)
(mngraph, mnglobalCredibility) = gmm.rankCredibility(mngraph)
gmm.printRank(mngraph)
mngFinalScore = gmm.globaliscore(msids,mhids,mnormalizedSysPer, mnglobalCredibility, -1)

mq.printFinalScore(mugFinalScore, 'Global')
mq.printFinalScore(mngFinalScore, 'Normalized_Global')
mq.printGlobalCredibility(mhids.keys(), mglobalCredibility, 'un_normalized')
mq.printGlobalCredibility(mhids.keys(), mnglobalCredibility, 'normalized')



