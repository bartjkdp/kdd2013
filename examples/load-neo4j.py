"""
load-neo4j.py
Bart J - 2014-06-02.
This script loads the CSV database in Neo4j
"""
import csv
from py2neo import neo4j, rel

graph_db = neo4j.GraphDatabaseService()

authorIndex = graph_db.get_or_create_index(neo4j.Node, "Author")
paperIndex = graph_db.get_or_create_index(neo4j.Node, "Paper")
conferenceIndex = graph_db.get_or_create_index(neo4j.Node, "Conference")
journalIndex = graph_db.get_or_create_index(neo4j.Node, "Journal")

# =====================================================================================
# Author
# =====================================================================================
fread = open('../data/Author-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

#for i,data in enumerate(reader):
	#authorIndex.get_or_create('Id', int(data['Id']), {'Name': data['Name'], 'Affiliation': data['Affiliation']})
fread.close()

# =====================================================================================
# Conference
# =====================================================================================
fread = open('../data/Conference-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

#for i,data in enumerate(reader):
	#conferenceIndex.get_or_create('Id', int(data['Id']), {'ShortName': data['ShortName'], 'FullName': data['FullName'], 'HomePage': data['HomePage']})
fread.close()

# =====================================================================================
# Journal
# =====================================================================================
fread = open('../data/Journal-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

#for i,data in enumerate(reader):
	#journalIndex.get_or_create('Id', int(data['Id']), {'ShortName': data['ShortName'], 'FullName': data['FullName'], 'HomePage': data['HomePage']})
fread.close()

# =====================================================================================
# Paper
# =====================================================================================
fread = open('../data/Paper-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

for i,data in enumerate(reader):
	paper = paperIndex.get_or_create('Id', int(data['Id']), {'Title': data['Title'], 'Year': data['Year'], 'Keyword': data['Keyword']})

	if data['ConferenceId']:
		conference = conferenceIndex.get('Id', int(data['ConferenceId']))
		#if len(conference) > 0:
			#graph_db.create(rel(paper, "PublishedIn", conference[0]))
		
	if data['JournalId']:
		journal = journalIndex.get('Id', int(data['JournalId']))
		#if len(journal) > 0:
			#graph_db.create(rel(paper, "PublishedIn", journal[0]))
fread.close()

# =====================================================================================
# PaperAuthor
# =====================================================================================
fread = open('../data/PaperAuthor-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

for i,data in enumerate(reader):
	paper = paperIndex.get('Id', int(data['PaperId']))
	author = authorIndex.get('Id', int(data['AuthorId']))

	if len(author) > 0 and len(paper) > 0:
		graph_db.create(rel(author[0], "Wrote", paper[0]))
fread.close()