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
from sklearn.metrics.pairwise import linear_kernel
from math import sqrt
from numpy.linalg import norm
from numpy import mean

def allFeatures(authorId, paperId):
	features = []

	# Normal count and percentage attributes
	#features.append(numberOfAuthorPaperPairs(authorId, paperId))
	#features.append(numberAuthors(authorId, paperId))
	#features.append(papersSameJournal(authorId, paperId))	
	#features.append(commonAffiliations(authorId, paperId))

	# Text related attributes (distances & counts)
	#features.append(jaroWinklerDistanceAuthorPaper(authorId, paperId))
	#features.append(jaroWinklerDistanceAffiliation(authorId, paperId))	
	#features.append(countVectPaperAuthorPapers(authorId, paperId))

	# Network analysis attributes
	#features.append(hetesimAPV(authorId, paperId))	
	#features.append(hetesimAPAPV(authorId, paperId))
	features.append(hetesimAPMAP(authorId, paperId))

	return features

def numberOfAuthorPaperPairs(authorId, paperId):
	authors = __builtin__.authors
	authorpaper = __builtin__.authorpaper
	return authorpaper[authorId].count(paperId)

def numberAuthors(authorId, paperId):
	return len(paperauthor[paperId])

def papersSameJournal(authorId, paperId):
	authors = __builtin__.authors
	authorpaper = __builtin__.authorpaper

	venueId = papers[paperId]['venueId']
	if not venueId:
		return 0

	count = 0
	for paperid in authorpaper[authorId]:
		if paperid in papers and papers[paperid]['venueId'] == venueId:
			count += 1

	return count

def commonAffiliations(authorId, paperId):
	paperauthor = __builtin__.paperauthor
	
	paperWords = paperauthor[paperId][authorId]['affiliation'].split()

	if len(paperWords) == 0:
		return 0

	average = []
	for author in paperauthor[paperId]:
		average.append(len(set(paperWords) & set(paperauthor[paperId][author]['affiliation'].split())) / len(paperWords))

	return mean(average)

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

def countVectPaperAuthorPapers(authorId, paperId):
	corpus = __builtin__.corpus
	return mean(linear_kernel(corpus[paperId], corpus[authorpaper[authorId]]).flatten())

def hetesimAPV(authorId, paperId):
	if paperId not in __builtin__.papers:
		return 0.5
	
	venueId = __builtin__.papers[paperId]['venueId']

	if venueId == 0:
		return 0.5	
	
	graph_hetesim_apv = __builtin__.graph_hetesim_apv
	return graph_hetesim_apv[authorId, venueId]

def hetesimAPAPV(authorId, paperId):
	if paperId not in __builtin__.papers:
		return 0.5
	
	venueId = __builtin__.papers[paperId]['venueId']

	if venueId == 0:
		return 0.5	

	graph_hetesim_apapv = __builtin__.graph_hetesim_apapv
	return graph_hetesim_apapv[authorId, venueId]

def hetesimAPMAP(authorId, paperId):
	graph_hetesim_apmap __builtin__.graph_hetesim_apmap
	return graph_hetesim_apmap[authorId, paperId]