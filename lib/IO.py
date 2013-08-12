import csv
import marshal
import os.path
import PreProcess

from ProgressBar import *

from collections import defaultdict
from collections import OrderedDict
from itertools import groupby

def readAuthors():
	print 'Reading authors...'

	if os.path.isfile('memory/authors.m'):
		f = open("memory/authors.m","rb")
		return marshal.load(f)
		f.close()

	f = open('data/Author.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	authors = {}
	
	for i,data in enumerate(reader):
		authors[int(data['Id'])] = {'name': data['Name'], 'affiliation': data['Affiliation']}
	f.close()
	
	print 'Dumping authors...'
	f = open("memory/authors.m","wb")
	marshal.dump(authors, f)
	f.close()
	
	return authors

def readVenues():
	print 'Reading venues...'
	
	if os.path.isfile('memory/venues.m'):
		f = open("memory/venues.m","rb")
		return marshal.load(f)
		f.close()

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
	
	print 'Dumping venues...'
	f = open("memory/venues.m","wb")
	marshal.dump(venues, f)
	f.close()
	
	return venues

def readPapers():
	print 'Reading papers...'
	
	if os.path.isfile('memory/papers.m'):
		f = open("memory/papers.m","rb")
		return marshal.load(f)
		f.close()
			
	f = open('data/Paper.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	papers = {}

	for i,data in enumerate(reader):
		if int(data['ConferenceId']) > 0:
			venueId = 'c' + str(int(data['ConferenceId']))
		elif int(data['JournalId']) > 0:
			venueId = 'j' + str(int(data['JournalId']))
		else:
			jcid = 0
 
		# data['Keyword'] not added yet
		papers[int(data['Id'])] = {'title': data['Title'], 'year': data['Year'], 'venueId': venueId, 'authors': [],'keywords': data['Keyword']}
		
	f.close()
	
	print 'Dumping papers...'
	f = open("memory/papers.m","wb")
	marshal.dump(papers, f)
	f.close()
	
	return papers
	
def readPaperAuthor():
	print 'Reading paper-author relationships...'
	
	if os.path.isfile('memory/paper-author.m'):
		f = open("memory/paper-author.m","rb")
		return marshal.load(f)
		f.close()
	
	f = open('data/PaperAuthor.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	
	count = 1
	paperauthor = {}
	
	for i,data in enumerate(reader):
		paperid = int(data['PaperId'])
		authorid = int(data['AuthorId'])		

		if paperid in paperauthor:
			paperauthor[paperid][authorid] = {'authorName': data['Name'], 'affiliation': data['Affiliation']}
		else:
			paperauthor[paperid] = {authorid: {'authorName': data['Name'], 'affiliation': data['Affiliation']}}
		
		# Keep user updated about the progress
		if count == 500000:
			print str(i)
			count = 1
		count += 1
		
	f.close()
	
	print 'Dumping paper-author relationships...'
	f = open("memory/paper-author.m","wb")
	marshal.dump(paperauthor, f)
	f.close()
	
	return paperauthor

def readAuthorPaper():
	print 'Reading author-paper relationships...'
	
	if os.path.isfile('memory/author-paper.m'):
		f = open("memory/author-paper.m","rb")
		return marshal.load(f)
		f.close()
	
	f = open('data/PaperAuthor.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)
	
	count = 1
	authorpaper = {}
	
	for i,data in enumerate(reader):
		paperid = int(data['PaperId'])
		authorid = int(data['AuthorId'])		

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
	
	print 'Dumping author-paper relationships...'
	f = open("memory/author-paper.m","wb")
	marshal.dump(authorpaper, f)
	f.close()
	
	return authorpaper

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
	return train

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

	return valid
    
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