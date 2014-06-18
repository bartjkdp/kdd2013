"""
generate-subset.py
Bart J - 2014-06-16.
This script generates a dataset will a small subset of the original dataset
"""
import csv

# =====================================================================================
# PaperAuthor
# =====================================================================================
fread = open('../data/PaperAuthor.csv')
fwrite = open('../data/PaperAuthor-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['PaperId','AuthorId','Name','Affiliation'])
writer.writeheader()

papers = []
authors = []

paperAuthorCount = 0;
prevPaperId = '';

for i,data in enumerate(reader):
	if prevPaperId != data['PaperId']:
		paperAuthorCount += 1;
	prevPaperId = data['PaperId']

	if paperAuthorCount > 10000:
		break

	if data['PaperId'] not in papers:
		papers.append(data['PaperId'])

	if data['AuthorId'] not in authors:
		authors.append(data['AuthorId'])

	writer.writerow({'PaperId': data['PaperId'], 'AuthorId': data['AuthorId'], 'Name': data['Name'], 'Affiliation': data['Affiliation']})

fwrite.close()
fread.close()

# =====================================================================================
# Author
# =====================================================================================
fread = open('../data/Author.csv')
fwrite = open('../data/Author-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['Id','Name','Affiliation'])
writer.writeheader()

for i,data in enumerate(reader):
	if data['Id'] not in authors:
		continue

	writer.writerow({'Id': data['Id'], 'Name': data['Name'], 'Affiliation': data['Affiliation']})

fwrite.close()
fread.close()

# =====================================================================================
# Paper
# =====================================================================================
conferences = []
journals = []

fread = open('../data/Paper.csv')
fwrite = open('../data/Paper-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['Id','Title','Year','ConferenceId','JournalId','Keyword'])
writer.writeheader()

for i,data in enumerate(reader):
	if data['Id'] not in papers:
		continue

	if data['ConferenceId'] and data['ConferenceId'] not in conferences:
		conferences.append(data['ConferenceId'])
	if data['JournalId'] and data['JournalId'] not in journals:
		journals.append(data['JournalId'])

	writer.writerow({'Id': data['Id'], 'Title': data['Title'], 'Year': data['Year'], 'ConferenceId': data['ConferenceId'], 'JournalId': data['JournalId'], 'Keyword':data['Keyword']})

fwrite.close()
fread.close()

# =====================================================================================
# Conference
# =====================================================================================
fread = open('../data/Conference.csv')
fwrite = open('../data/Conference-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['Id','ShortName','FullName','HomePage'])
writer.writeheader()

for i,data in enumerate(reader):
	if data['Id'] not in conferences:
		continue

	writer.writerow({'Id': data['Id'], 'ShortName': data['ShortName'], 'FullName': data['FullName'], 'HomePage': data['HomePage']})

fwrite.close()
fread.close()

# =====================================================================================
# Journal
# =====================================================================================
fread = open('../data/Journal.csv')
fwrite = open('../data/Journal-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['Id','ShortName','FullName','HomePage'])
writer.writeheader()

for i,data in enumerate(reader):
	if data['Id'] not in journals:
		continue

	writer.writerow({'Id': data['Id'], 'ShortName': data['ShortName'], 'FullName': data['FullName'], 'HomePage': data['HomePage']})

fwrite.close()
fread.close()

# =====================================================================================
# Train
# =====================================================================================
fread = open('../data/Train.csv')
fwrite = open('../data/Train-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['AuthorId','ConfirmedPaperIds','DeletedPaperIds'])
writer.writeheader()

for i,data in enumerate(reader):	
	if data['AuthorId'] not in authors:
		continue

	confirmed = list(set(data['ConfirmedPaperIds'].split()) & set(papers))
	deleted = list(set(data['DeletedPaperIds'].split()) & set(papers))

	confirmed = " ".join([str(x) for x in confirmed])
	deleted = " ".join([str(x) for x in deleted])

	writer.writerow({'AuthorId': data['AuthorId'], 'ConfirmedPaperIds': confirmed, 'DeletedPaperIds': deleted})

fwrite.close()
fread.close()

# =====================================================================================
# Valid
# =====================================================================================
fread = open('../data/Valid.csv')
fwrite = open('../data/Valid-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['AuthorId','PaperIds'])
writer.writeheader()

for i,data in enumerate(reader):	
	if data['AuthorId'] not in authors:
		continue

	paperids = list(set(data['PaperIds'].split()) & set(papers))
	paperids = " ".join([str(x) for x in paperids])

	writer.writerow({'AuthorId': data['AuthorId'], 'PaperIds': paperids})

fwrite.close()
fread.close()

# =====================================================================================
# ValidSolution
# =====================================================================================
fread = open('../data/ValidSolution.csv')
fwrite = open('../data/ValidSolution-subset.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['AuthorId','PaperIds','Usage'])
writer.writeheader()

for i,data in enumerate(reader):	
	if data['AuthorId'] not in authors:
		continue

	paperids = list(set(data['PaperIds'].split()) & set(papers))
	paperids = " ".join([str(x) for x in paperids])

	writer.writerow({'AuthorId': data['AuthorId'], 'PaperIds': paperids, 'Usage': data['Usage']})

fwrite.close()
fread.close()
