import os
import sys
from collections import defaultdict
import networkx as nx
import math

class globalimeasure:

    def __init__(self, name):

      self.name = name

    def findNeighbors(self,h,f,hids) :
        neighborListh = set()
    
        for h1 in hids.keys():
           if h1 != h  and f in hids[h1]:
               neighborListh.add(h1)
    
        return neighborListh
        
    def generatePairs(self, set1) :
            
            allPairs = set()
            
            for x in set1 :
                for y in set1:
                    if x != y :
                        allPairs.add((x,y))
                        allPairs.add((y,x))
            return allPairs


    def defineGraph(self, fileids, hids, gperformanceSet, index):

        graph = nx.DiGraph()
        participants = hids.keys()
        edge_pairs = self.generatePairs(participants)
        for p in participants:
            graph.add_node(p, crank = 0.001)
    
        for item in edge_pairs :
            graph.add_edge(item[0],item[1], cweight = 0.000)
             #print(n,'>> rank : ', graph.node[n]['crank'])


        fileK= set()
        
        for h in hids:
            files = hids[h]
            for f in files:
                if f not in fileK :
                    neighbors_h = self.findNeighbors(h,f,hids)
                    participants = neighbors_h.union(set([h]))
                    fileK.add(f)
                    #print('File: ', f)
                    #print('Node: ', h)
                    #print('Neighbors: ', neighbors_h)
                    edge_pairs = self.generatePairs(participants)
                    for e in edge_pairs:
                        if index > 0 :
                            initialCredibility = gperformanceSet[(e[0],e[1],f)][index]
                        else:
                            initialCredibility = gperformanceSet[(e[0],e[1],f)]
                        graph.edge[e[0]][e[1]]['cweight'] += initialCredibility

        highestEdgeWeight = 0.000
        for n in graph.nodes():
            outEdges_n = graph.out_edges(n)
            for (u,v) in outEdges_n :
                if graph.edge[u][v]['cweight'] >  highestEdgeWeight :
                    highestEdgeWeight = graph.edge[u][v]['cweight']


        
        #print graph
        for n1,n2,attr in graph.edges(data=True):
            attr['cweight'] = attr['cweight']/highestEdgeWeight
            #print(n1,',',n2,'>>', attr['cweight'])

        #print('No of Edges: ', graph.number_of_edges())
         
        return graph

    def rankCredibility(self,graph):


        sz = graph.number_of_edges()
        ns = graph.number_of_nodes()
        alpha = float(0.55)
        threshold = 0.01
        change = 0.1000

        #for n in graph.nodes() :
             #print(n, '>>', graph.node[n]['crank'] )


        for i in range(1, sz*100) :
           for n in graph.nodes():
               rank = 0.0000
               #print('current node = ', n)
               for p in graph.predecessors(n):
                     #print(p, ': out_degree = ', graph.out_degree(p), ' weight =',graph.edge[p][n]['cweight'])
                     rank += float (float(graph.edge[p][n]['cweight']) / float(graph.out_degree(p))) * graph.node[p]['crank']
                     #print('rank =', rank)
               if graph.in_degree(n) != 0 :
                     previous_rank = graph.node[n]['crank']
                     graph.node[n]['crank'] = float(1 - alpha)/ float(ns) + rank * alpha
                     #print('current rank = ', graph.node[n]['crank'])
                     n_rank_change = math.fabs(previous_rank - graph.node[n]['crank'])
                     #print('change = ', change)
                     if n_rank_change > change :
                        change = n_rank_change

           if change < threshold :
              break
        
        credibilityDict = defaultdict()
        for n in graph.nodes() :
            credibilityDict[n] = graph.node[n]['crank']
        
        return (graph, credibilityDict)


    def printRank(self,graph):
        rankList = defaultdict()
   
        for n in graph.nodes() :
              #print(n, '>>', graph.node[n]['crank'] )
              rankList[n] =    graph.node[n]['crank']
        sortedData = sorted(rankList.items(), key = lambda x: x[1], reverse = True)
        print(sortedData)    

    def scoreS(self, f, s, neighborList, sperformanceSet, credibilityDict, index):

        score_s = 0.00
    
        for n in neighborList :
            if index >= 0 :
                 score_s += credibilityDict[n] * sperformanceSet[(s,n,f)][5]
            else:
                 score_s += credibilityDict[n] * sperformanceSet[(s,n,f)]
        iscore_s = float(score_s) / float(len(neighborList))

        return iscore_s


    def globaliscore(self, sids,hids, systemPerformance, credibilityDict, index) :
    
        iscoreGlobal = defaultdict()
        iscore = defaultdict()
        for s in sids.keys() :
           fileList = sids[s]
           iscoreTotal = 0.00
           for f in fileList :
              sneighbors = self.findNeighbors(s,f,hids)
              iscores = self.scoreS(f,s,sneighbors,systemPerformance,credibilityDict, index)
              iscoreGlobal[(s,f)] = iscores
              iscoreTotal += iscores
           iscore[s] = float(iscoreTotal)/ float(len(fileList))
    
        return iscore












