"""
InitialCalculation.py
Bart J - 2014-06-19.
KDD Cup 2013 Track 1
"""
from __future__ import division
import __builtin__
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import coo_matrix, csr_matrix, dok_matrix
import itertools

def calculate():
	calculateAdjecency()
	#calculateCountVectorizer()

def calculateAdjecency():
	print 'Generating adjecency and probability transition matrixes...'
	ap = __builtin__.graphAuthorpaper
	prob_ap = normalize(ap,norm='l1',axis=1)
	vp = __builtin__.graphVenuepaper
	prob_vp = normalize(vp,norm='l1',axis=1)

	# HeteSim A-P-V (identical to A-P-V-P)
	__builtin__.graph_hetesim_apv = prob_ap.dot(prob_vp.transpose())

	# HeteSim A-P-M-A-P (similarity through co-author)
	pa = ap.transpose()
	prob_pa = normalize(pa,norm='l1',axis=1)

	#[pm, ma] = createMiddleObject(pa)
	pm = __builtin__.pm
	ma = __builtin__.ma
	prob_pm = normalize(pm,norm='l1',axis=1)

	am = ma.transpose()
	prob_am = normalize(am,norm='l1',axis=1)
	
	prob_appm = prob_ap.dot(prob_pm)
	prob_paam = prob_pa.dot(prob_am)

	__builtin__.graph_hetesim_apmap = prob_appm.dot(prob_paam.transpose())

	# HeteSim A-P-A-P-V (similarity through co-author published in the same venue)
	prob_appa = prob_ap.dot(prob_pa)
	prob_vppa = prob_vp.dot(prob_pa)

	__builtin__.graph_hetesim_apapv = prob_appa.dot(prob_vppa.transpose())

def createMiddleObject(mat):
	mat = coo_matrix(mat)

	m1 = dok_matrix((mat.shape[0],len(mat.data)))
	m2 = dok_matrix((len(mat.data),mat.shape[1]))

	i=0
	for j,k,v in itertools.izip(mat.row, mat.col, mat.data):
		m1[j,i] = 1
		m2[i,k] = 1
		i+=1

	return [m1.tocsr(), m2.tocsr()]

def calculateCountVectorizer():
	print 'Generating count vectorizer...'
	corpus = []
	for paper in papers:
		corpus.append(papers[paper]['title'].lower() + ' ' + papers[paper]['keywords'].lower())

	vectorizer = CountVectorizer(binary=True, stop_words="english")
	corpus = vectorizer.fit_transform(corpus)
	__builtin__.corpus = corpus
