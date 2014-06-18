"""
IO.py
Bart J - 2014-06-01.
KDD Cup 2013 Track 1
"""

import csv
import marshal
import numpy as np
import os.path
import PreProcess
import __builtin__
import scipy.io as sio
from scipy.sparse import csr_matrix
from scipy.sparse import dok_matrix
from collections import defaultdict
from collections import OrderedDict

def readAuthors():
	print 'Reading authors...'

	authors = readCache('authors')
	if not authors:
		f = open('data/Author.csv')
		reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
		authors = {}
		
		for i,data in enumerate(reader):
			authors[int(data['Id'])] = {'name': data['Name'], 'affiliation': data['Affiliation']}
		f.close()
		writeCache('authors', authors)

	__builtin__.authors = authors
	return True

def readVenues():
	print 'Reading venues...'
	
	venues = readCache('venues')
	if not venues:
		f = open('data/Journal.csv')
		reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
		venues = {}
	        
		for i,data in enumerate(reader):
			venues['j' + str(data['Id'])] = {'sname': data['ShortName'], 'name': data['FullName']}

		f = open('data/Conference.csv')
		reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
		
		for i,data in enumerate(reader):
			venues['c' + str(data['Id'])] = {'sname': data['ShortName'], 'name': data['FullName']}
		
		f.close()
		writeCache('venues', venues)
	
	__builtin__.venues = venues
	return True

def readPapers():
	print 'Reading papers...'
				
	papers = readCache('papers')
	graphVenuepaper = readCache('graphVenuepaper')

	if not papers:
		f = open('data/Paper.csv')
		reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
		
		papers = {}
		graphVenuepaper = dok_matrix((2500000,2500000))

		for i,data in enumerate(reader):
			if int(data['JournalId']) > 0:
				venueId = int(data['JournalId'])
			elif int(data['ConferenceId']) > 0:
				venueId = 25000 + int(data['ConferenceId'])
			else:
				venueId = 0
	 
			paperId = int(data['Id'])

			papers[paperId] = {'title': data['Title'], 'year': data['Year'], 'venueId': venueId, 'authors': [],'keywords': data['Keyword']}
			
			if venueId is not 0:
				graphVenuepaper[venueId, paperId] = 1

		f.close()

		graphVenuepaper = graphVenuepaper.tocsr()		

		writeCache('papers', papers)
		writeCache('graphVenuepaper', graphVenuepaper)

	__builtin__.papers = papers
	__builtin__.graphVenuepaper = graphVenuepaper

	return True
	
def readAuthorPaper():
	print 'Reading author-paper relationships...'
	
	authorpaper = readCache('authorpaper')
	graphAuthorpaper = readCache('graphAuthorpaper')
	paperauthor = readCache('paperauthor')

	if not authorpaper:
		f = open('data/PaperAuthor.csv')
		reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
		
		count = 1
		graphAuthorpaper = dok_matrix((2500000,2500000))
		authorpaper = {}
		paperauthor = {}

		for i,data in enumerate(reader):
			paperid = int(data['PaperId'])
			authorid = int(data['AuthorId'])		
			graphAuthorpaper[authorid, paperid] = 1

			if paperid not in paperauthor:
				paperauthor[paperid] = {}
			
			paperauthor[paperid][authorid] = {'authorName':data['Name'], 'affiliation':data['Affiliation']}

			if authorid in authorpaper:
				authorpaper[authorid].append(paperid)
			else:
				authorpaper[authorid] = [paperid]

			# Keep user updated about the progress
			if count == 500000:
				print str(i)
				count = 1

			count += 1
		f.close()

		graphAuthorpaper = graphAuthorpaper.tocsr()	
		
		writeCache('authorpaper', authorpaper)
		writeCache('paperauthor', paperauthor)
		writeCache('graphAuthorpaper', graphAuthorpaper)		

	__builtin__.graphAuthorpaper = graphAuthorpaper
	__builtin__.paperauthor = paperauthor
	__builtin__.authorpaper = authorpaper

	return True

def readCache(type):
	if os.path.isfile('memory/' + type + '.m'):
		f = open('memory/' + type + '.m','rb')
		return marshal.load(f)
		f.close()
	elif os.path.isfile('memory/' + type + '.npz'):
		load = np.load('memory/' + type + '.npz')
		return csr_matrix((load['data'], load['indices'], load['indptr']), shape = load['shape'])
	else:
		return False

def writeCache(type, variable):
	print 'Dumping ' + type

	if isinstance(variable, dok_matrix) or isinstance(variable, csr_matrix):
		np.savez('memory/' + type, data=variable.data, indices=variable.indices, indptr=variable.indptr, shape=variable.shape)
	else:
		f = open('memory/' + type + '.m','wb')
		marshal.dump(variable, f)
		f.close()

def readTrainData():
	print 'Reading train data...'
	# Return values on papers of the training-set

	f = open('data/Train.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	train = []

	for i,data in enumerate(reader):
		for id in data['ConfirmedPaperIds'].split():
			train.append({'label': 1, 'paperId': int(id), 'authorId': int(data['AuthorId'])})

		for id in data['DeletedPaperIds'].split():
			train.append({'label': 0, 'paperId': int(id), 'authorId': int(data['AuthorId'])})
	
	f.close()
	
	__builtin__.trainData = train
	return True

def readValidData():
	print 'Reading valid data...'
	# Return values on papers of the validation-set

	f = open('data/Valid.csv')

	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	valid = []

	for i,data in enumerate(reader):
		for id in data['PaperIds'].split():
			valid.append({'paperId': int(id), 'authorId': int(data['AuthorId'])})
	f.close()

	__builtin__.validData = valid
	return True

def writePredictions(predictions, validData):
	authorPredictions = defaultdict(list)

	# Read all predictions in a defaultdict and put them in the form authorid[(prediction, paperid), (prediction2, paperid2)]
	for row,prediction in zip(validData, predictions):
        	authorPredictions[row['authorId']].append((prediction, row['paperId']))

	# Order predictions on authorid
	authorPredictions = OrderedDict(sorted(authorPredictions.items(), key=lambda t:t[0]))

	# Sort list of paper ID's on probabilities and remove probability from tuple
	for authorId in authorPredictions:
        	paperIdsSorted = sorted(authorPredictions[authorId], reverse=True)
	        authorPredictions[authorId] = [x[1] for x in paperIdsSorted]

	# Write predictions to CSV
	f = open('data/ValidPredicted.csv','wb')
	writer = csv.DictWriter(f, delimiter=',', fieldnames=['AuthorId','PaperIds'])
	writer.writeheader()

	for authorId in authorPredictions:
        	paperIds = " ".join([str(x) for x in authorPredictions[authorId]])
	        writer.writerow({'AuthorId': authorId, 'PaperIds': paperIds})

	f.close()