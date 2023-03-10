# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 19:02:54 2022

@author: Wesley.Nijmeijer
"""

import csv
import itertools
import matplotlib.pyplot as plt
import math
import networkx as nx
import numpy as np
import pandas as pd
import random
import time


"""
=============================================================================
Input variables
=============================================================================
"""

#defining the file containing the trajects on which a hydrogen pipeline can be
#constructed
file_allroutes = 'edges.txt'
#file_allroutes = 'edges_daadwerkelijk2.txt'

#possible capacities for new pipelines
cap = [10,20,30] #Different capacities

#cost for new pipeline construction

c1 = 10 #Cost of the construction of 1 km of pipeline with capacity 10
Rc = 1.3 #increase in cost if the capacity of a new pipeline doubles

#%%
"""
=============================================================================
Timing the calculations
=============================================================================
"""

starttime = time.time()

#%%
"""
=============================================================================
Reading txt file containing possible pipeline trajects and plotting graph with all possible trajects
=============================================================================
"""

g = nx.read_edgelist(file_allroutes, create_using=nx.MultiDiGraph(), nodetype = int)
nx.draw(g, with_labels=True, connectionstyle='arc3, rad=0.1')
plt.show()

n = g.number_of_edges()
N = g.number_of_nodes()
E = list(g.edges()) #All edges in an ordered list

print('Er zijn in totaliteit', n ,'mogelijke trajecten. Deze trajecten verbinden', N, 'knopen.')

#Determining trajects which need to be included as they are essential for the network to be connected
EP = []     #list of the indexes of the essential pipelines in list E

for i in range(N):
    if g.degree(i) == 1: 
        EP += (E.index((u, v)) for u,v in g.in_edges(i))
        EP +=  (E.index((u, v)) for u,v in g.out_edges(i))
        
if EP == []:
    print('er zijn geen essenti??le pijpleidingen in de volledige graaf')
else:
    print('de essenti??le pijpleidingen in de volledige graaf zijn:', [E[i] for i in EP])  

#%%
"""
=============================================================================
Determining scenario
=============================================================================
"""

scenario = {i:random.randint(-5,5) for i in range(N-1)}
scenario[N-1] = -sum(scenario.values())
df_demand = pd.DataFrame.from_dict(scenario, orient='index', columns=['Demand'])

#Total demand to be satisfied
total_demand = sum([scenario[i] for i in range(N) if scenario[i]>0])

#%%
"""
=============================================================================
Determining length of trajects
=============================================================================
"""

length = {E[i]:random.randint(10,100) for i in range(n)}


#%%

"""
=============================================================================
Determining variants with whether or not a pipeline exists
=============================================================================
"""

trajects = []

for i in range(n):
    if i in EP:
        trajects.append([1])
    else:
        trajects.append([0,1])

#%%
"""
=============================================================================
Determining variants and caluclating costst of and maximal flows through the network
=============================================================================
"""

k = len(cap) #Number of different capacities


file = open('test.csv', 'w', newline='')
writer = csv.writer(file, delimiter=',')
writer.writerow(["v", "c","flow_value", "costs"])

plot = np.array([[],[]]) # start of array with x (costs) and y (maximal flows) of the different variants

x = []
y = []

for v in itertools.product(*trajects):
    n1 = v.count(1) #number of edges in graph
    if n1 >= N-1:
        G = nx.Graph([E[n-1-i] for i in range(len(v)) if v[i]== 1]) #Define graph
        G.add_nodes_from(list(range(N))) #Add all nodes
        l_N = list(G.nodes())
        if nx.is_connected(G):
            GE = list(G.edges()) #list of edges in G
            capacities = [[0,1,2] for i in range(n1)]
            for c in itertools.product(*capacities):
                cap_e = {GE[i]: cap[c[i]] for i in range(len(capacities))}
                nx.set_edge_attributes(G,cap_e,'capacity')
                # Demand of nodes
                nx.set_node_attributes(G,scenario,'demand')
                # Length of edges 
                nx.set_edge_attributes(G,length, 'length')
                # Calculating costs of the network
                costs = 0
                for i in range(G.number_of_edges()):
                    costs += G[GE[i][0]][GE[i][1]]['length']*c1*(G[GE[i][0]][GE[i][1]]['capacity']/cap[0])*Rc
                costs = round(costs)
                x.append(costs)
                # Make directed graph
                H = G.to_directed()
                # Apply maximum flow to find the maximum flow through the network
                H.add_nodes_from(['supersource', 'supersink'])
                for i in range(len(l_N)):
                    if H.nodes[i]['demand'] < 0:
                        H.add_edge('supersource',i, capacity = math.inf)
                    elif H.nodes[i]['demand'] > 0:
                        H.add_edge(i, 'supersink', capacity = math.inf)
                flow_value = nx.maximum_flow(H, 'supersource', 'supersink')[0]
                y.append(round(flow_value))
                writer.writerow([v,c,flow_value, costs])

file.close()

#%%
"""
=============================================================================
Calculating the pareto front
=============================================================================
"""

sorted_list = sorted([[x[i], y[i]] for i in range(len(x))])
start = [sorted_list[0]]

for pair in sorted_list:
    if pair[0] == start[0][0]:
        if pair[1] > start[0][1]:
                start.clear()
                start.append(pair)
     
pareto_front = []

for pair in sorted_list:
    if pair == start[0]:
        pareto_front.append(pair)

for pair in sorted_list:
    if pair != start[0] and pair[1] >= pareto_front[-1][1]:
        if pair[0] == pareto_front[-1][0] and pair != pareto_front[-1]:
            pareto_front.remove(pareto_front[-1])
            pareto_front.append(pair)
        elif pair == pareto_front[-1]:
            pareto_front.append(pair)
        elif pair[0] >= pareto_front[-1][0] and pair[1] <= pareto_front[-1][1]:
            pass
        else:
            pareto_front.append(pair)
                    

print(pareto_front)

plt.plot(x, y, '.b', markersize=16, label='Non Pareto-optimal')
pf_x = [pair[0] for pair in pareto_front]
pf_y = [pair[1] for pair in pareto_front]
plt.plot(pf_x, pf_y, '.r', markersize=16, label='Pareto optimal')
plt.xlabel("Costs", fontsize=16)
plt.ylabel("Maximum flow", fontsize =16)
plt.legend(loc=3, numpoints=1)
plt.show()
         
#%%
"""
=============================================================================
Timing the calculations
=============================================================================
"""

endtime = time.time()
print('de berekeningen duurden', round((endtime-starttime)), 'seconden.')