from __future__ import division
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import scipy
import numpy as np
from math import sqrt

graph = nx.Graph()
graph.add_node("a1", type="a")
graph.add_node("a2", type="a")
graph.add_node("a3", type="a")

graph.add_node("b1", type="b")
graph.add_node("b2", type="b")
graph.add_node("b3", type="b")
graph.add_node("b4", type="b")

graph.add_edge("a1", "b1")
graph.add_edge("a1", "b2")
graph.add_edge("a2", "b2")
graph.add_edge("a2", "b3")
graph.add_edge("a2", "b4")
graph.add_edge("a3", "b4")


ae = np.mat('[0.5 0.5 0 0 0 0;0 0 0.33 0.33 0.33 0;0 0 0 0 0 1]')
eb = np.mat('[1 0 0 0;0 0.5 0 0; 0 0.5 0 0;0 0 1 0;0 0 0 0.5;0 0 0 0.5]')
ab = np.mat('[0.5 0.5 0 0; 0 0.33 0.33 0.33; 0 0 0 1]')
	

# HeteSim(A,B|AB), before normalization
#print ae * eb

# HeteSim(A,A|ABA), before normalization
#print ab * ab.transpose()

# HeteSim(A,A|ABA), after normalization
print cosine_similarity(ab[0,:], ab[0,:].transpose().transpose())