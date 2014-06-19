"""
InitialCalculation.py
Bart J - 2014-06-19.
KDD Cup 2013 Track 1
"""
from __future__ import division
import __builtin__
from sklearn.preprocessing import normalize
from sklearn.feature_extraction.text import CountVectorizer
from scipy.sparse import csr_matrix
import itertools

def calculate():
	calculateAdjecency()
	calculateCountVectorizer()

def calculateAdjecency():
	print 'Generating adjecency and probability transition matrixes...'
	ap = __builtin__.graphAuthorpaper
	pap = normalize(ap,'l2',1)

	pa = ap.transpose()
	ppa = normalize(pa,'l2',1)

	vp = __builtin__.graphVenuepaper
	pvp = normalize(vp,'l2',1)

	[pm, ma] = createMiddleObject(pa)
	
	ppm = normalize(pm,'l2',1)
	pma = normalize(ma,'l2',1)

	am = ma.transpose()
	pam = normalize(am,'l2',1)

	# Translate adjecency matrix to probability transition matrix
	__builtin__.graphPap = pap
	__builtin__.graphPpa = ppa
	__builtin__.graphPvp = pvp

	pappm = pap.dot(ppm)
	ppaam = ppa.dot(pam)

	__builtin__.graphPappmpaam = pappm.dot(ppaam.transpose())
	__builtin__.graphPapvp = pap.dot(pvp.transpose())

def createMiddleObject(matrix):
	matrix = matrix.tocoo()

	m1 = csr_matrix((matrix.shape[0],len(matrix.data)))
	m2 = csr_matrix((len(matrix.data),matrix.shape[1]))

	i=0
	for j,k,v in itertools.izip(matrix.row, matrix.col, matrix.data):
		m1[j,i] = 1
		m2[i,k] = 1
		i+=1

	return [m1, m2]

def calculateCountVectorizer():
	print 'Generating count vectorizer...'
	corpus = {}
	for paper in papers:
		corpus.append(papers[paper]['title'].lower() + ' ' + papers[paper]['keywords'].lower())

	vectorizer = CountVectorizer(binary=True, stop_words="english")
	corpus = vectorizer.fit_transform(corpus)
	__builtin__.corpus = corpus
