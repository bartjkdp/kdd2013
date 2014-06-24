"""
hetesim.py
Bart J - 2014-06-01.
Calculate Hetesim measure on toy example
"""

# This code replicates the example in the paper
# Shi, Chuan, et al. "Relevance search in heterogeneous networks." Proceedings of the 15th International Conference on Extending Database Technology. ACM, 2012.
# Paragraph 4.4

from __future__ import division
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize
import numpy as np

ae = np.mat('[1.0 1.0 0 0 0 0;0 0 1.0 1.0 1.0 0; 0 0 0 0 0 1.0]')
eb = np.mat('[1.0 0 0 0; 0 1.0 0 0; 0 1.0 0 0; 0 0 1.0 0; 0 0 0 1.0; 0 0 0 1.0]')
be = eb.transpose();

ap = np.mat('[1 1 0 0; 0 0 1 0; 0 1 0 1]')
vp = np.mat('[1 0 0 0; 0 1 1 0; 0 0 1 0]')

pap = ap/ap.sum(axis=1)
pvp = vp/vp.sum(axis=1)

ab = ae * eb;

# HeteSim(A,B|AB), before normalization
pae = (ae/ae.sum(axis=1))
pbe = (be/be.sum(axis=1))
pae = normalize(ae,norm='l1',axis=1)
pbe = normalize(be,norm='l1',axis=1)
#print pae * pbe.transpose()

# HeteSim(A,A|ABA), before normalization
pab = (ab/ab.sum(axis=1))
#print pab * pab.transpose()

# HeteSim(A,B|AB), after normalization
#print cosine_similarity(pae, pbe)

# HeteSim(A,A|ABA), after normalization
print cosine_similarity(pab, pab)
#print cosine_similarity(pab[1,:], pab[0,:])
#print cosine_similarity(pap,pvp)
