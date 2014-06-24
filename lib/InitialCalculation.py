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
from sklearn.metrics.pairwise import cosine_similarity
import itertools
import IO

def calculate():
	calculateAdjecency()
	calculateCountVectorizer()

def calculateAdjecency():
	print 'Generating adjecency and probability transition matrixes...'

	# HeteSim A-P-V (identical to A-P-V-P) (similarity through author published in same venue)
	ap = __builtin__.graphAuthorpaper
	vp = __builtin__.graphVenuepaper
	
	prob_ap = normalize(ap,norm='l1')
	prob_vp = normalize(vp,norm='l1')

	__builtin__.graph_hetesim_apv = cosine_similarity(prob_ap,prob_vp)

	# HeteSim A-P-A-P-V (similarity through co-author published in the same venue)
	prob_appa = prob_ap.dot(prob_pa)
	prob_vppa = prob_vp.dot(prob_pa)

	__builtin__.graph_hetesim_apapv = cosine_similarity(prob_appa,prob_vppa)

	# HeteSim A-P-M-A-P (similarity through co-authors)
	[pm, ma] = createMiddleObject(pa)

	#pm = IO.readCache('pm')
	#ma = IO.readCache('ma')
	authorpaper = IO.readCache('authorpaper')
	paperauthor = IO.readCache('paperauthor')

	# Make matrix more sparse to survive computation
	keepAuthors = []
	keepPapers = []

	trainData = __builtin__.trainData
	validData = __builtin__.validData	
	for trainItem in trainData:
		if trainItem['authorId'] not in keepAuthors:
			keepAuthors.append(trainItem['authorId'])
		if trainItem['paperId'] not in keepPapers:
			keepPapers.append(trainItem['paperId'])
	for validItem in validData:
		if validItem['authorId'] not in keepAuthors:
			keepAuthors.append(validItem['authorId'])
		if validItem['paperId'] not in keepPapers:
			keepPapers.append(validItem['paperId'])

	ap = dok_matrix((2500000,2500000))
	for author in keepAuthors:
		if author in authorpaper:
			for paper in authorpaper[author]:
				ap[author,paper] = 1


	pa = dok_matrix((2500000,2500000))
	for paper in keepPapers:
		if paper in paperauthor:
			for author in paperauthor[paper]:
				pa[paper,author] = 1

	ap = ap.tocsr()
	pa = pa.tocsr()
	am = ma.transpose()

	prob_ap = normalize(ap,norm='l1')
	prob_pm = normalize(pm,norm='l1')

	prob_pa = normalize(pa,norm='l1')
	prob_am = normalize(am,norm='l1')

	prob_appm = prob_ap.dot(prob_pm)
	prob_paam = prob_pa.dot(prob_am)

	__builtin__.graph_hetesim_apmap = cosine_similarity(prob_appm,prob_paam)

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
