"""
PreProcess.py
Bart J - 2014-06-01.
KDD Cup 2013 Track 1
"""
import nltk
import unicodedata

def clean_fields(entity, fields):
	for field in fields:
		entity[field] = nltk.clean_html(entity[field])		
		entity[field] = unicodedata.normalize('NFKD', unicode(entity[field], 'utf8')).encode('ascii','ignore')
		entity[field] = entity[field].replace(',','').replace(';','').replace('|',' ').replace('?','')
		entity[field] = entity[field].lower()		
	return entity

def authors(authors):
	print 'Preprocessing authors...'
	for author in authors:
		authors[author] = clean_fields(authors[author], ['name','affiliation'])
	return authors

def papers(papers):
	print 'Preprocessing papers...'
	for paper in papers:
		papers[paper] = clean_fields(papers[paper], ['title','keywords'])
		keywords = papers[paper]['keywords'] 
		keywords.replace('keywords:','').replace('keywords','').replace('key-words: - ','').replace('key words: ','')
		papers[paper]['keywords'] = keywords
	return papers
	
def venues(venues):
	print 'Preprocessing venues...'
	for venue in venues:
		venues[venue] = clean_fields(venues[venue], ['sname','name'])
	return venues

def paperauthors(paperauthors):
	print 'Preprocessing paperauthors...'
	for paper in paperauthors:
		for author in paperauthors[paper]:
			paperauthors[paper][author] = clean_fields(paperauthors[paper][author], ['authorName','affiliation'])
	return paperauthors