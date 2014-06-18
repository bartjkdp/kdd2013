"""
GenerateFeatures.py
Bart J - 2014-06-01.
KDD Cup 2013 Track 1
"""

from __future__ import division
import IO
import jellyfish
import numpy as np
import nltk
import __builtin__
from sklearn.feature_extraction.text import TfidfVectorizer	
from sklearn.metrics.pairwise import cosine_similarity
from math import sqrt
from numpy.linalg import norm

def allFeatures(authorId, paperId):
	features = []

	features.append(numberOfAuthorPaperPairs(authorId, paperId))
	features.append(jaroWinklerDistanceAuthorPaper(authorId, paperId))
	features.append(jaroWinklerDistanceAffiliation(authorId, paperId))	
	#features.append(publicationYearDiff(authorId, paperId))
	#features.append(hetesimAPV(authorId, paperId))
	#features.append(hetesimAPVP(authorId, paperId))
	#features.append(tfidfPaperAuthorPapers(authorId, paperId))

	return features

def numberOfAuthorPaperPairs(authorId, paperId):
	authors = __builtin__.authors
	authorpaper = __builtin__.authorpaper
	return authorpaper[authorId].count(paperId)

def jaroWinklerDistanceAuthorPaper(authorId, paperId):
	authors = __builtin__.authors
	paperauthor = __builtin__.paperauthor

	if authors[authorId]['name'] and paperauthor[paperId][authorId]['authorName']:
		return jellyfish.jaro_distance(authors[authorId]['name'], 
								       paperauthor[paperId][authorId]['authorName'])
	else:
		return 0.5
		
def jaroWinklerDistanceAffiliation(authorId, paperId):
	authors = __builtin__.authors
	paperauthor = __builtin__.paperauthor

	if authors[authorId]['name'] and paperauthor[paperId][authorId]['authorName']:
		return jellyfish.jaro_distance(authors[authorId]['affiliation'], 
								       paperauthor[paperId][authorId]['affiliation'])
	else:
		return 0.5

def publicationYearDiff(authorId, paperId):
	authorpaper = __builtin__.authorpaper
	papers = __builtin__.papers

	paperids = authorpaper[authorId]
	years = []
	for paperid in paperids:
		if paperid not in papers:
			continue
		if papers[paperid]['year']:
			years.append(int(papers[paperid]['year']))

	if len(years) == 0 or int(papers[paperId]['year']) == 0:
		return 0
	else:
		return abs((sum(years)/len(years)) - int(papers[paperId]['year']))

def hetesimAPV(authorId, paperId):
	if paperId not in __builtin__.papers:
		return 0.5
	
	venueId = __builtin__.papers[paperId]['venueId']

	if venueId == 0:
		return 0.5	
	
	pappv = __builtin__.graphPappv

	return pappv[paperId,venueId]

def hetesimAPVP(authorId, paperId):
	if paperId not in __builtin__.papers:
		return 0.5

	venueId = __builtin__.papers[paperId]['venueId']

	if venueId == 0:
		return 0.5

	pap = __builtin__.graphPap
	pvp = __builtin__.graphPvp

	return cosine_similarity(pap[authorId,:],pvp[venueId,:])


__builtin__.authorTfidf = {}
def tfidfPaperAuthorPapers(authorId, paperId):
	global authorTfidf

	if authorId not in __builtin__.authorTfidf:
		papers = __builtin__.papers
		authorpaper = __builtin__.authorpaper

		stopwords = nltk.corpus.stopwords.words('english')
		vectorizer = TfidfVectorizer(stop_words = stopwords, min_df=1)

		analyse = []
		for paper in authorpaper[authorId]:
			analyse.append(papers[paper]['title'] + ' ' + papers[paper]['keywords'])

		vectorizer.fit_transform(analyse)
		authorTfidf[authorId] = vectorizer

	vectorizer = authorTfidf[authorId]

	analyse = []
	for paper in authorpaper[authorId]:
		analyse.append(papers[paper]['title'] + ' ' + papers[paper]['keywords'])

	currentAuthorPapers = vectorizer.transform(analyse)
	currentPaper = vectorizer.transform(papers[paperId]['title'] + ' ' + papers[paperId]['keywords'])
	
	cosSim = 0
	i = 0

	for currentAuthorPaper in currentAuthorPapers:
		cosSim = cosSim + float(cosine_similarity(currentPaper, currentAuthorPaper))
		i = i + 1

	return cosSim/i
