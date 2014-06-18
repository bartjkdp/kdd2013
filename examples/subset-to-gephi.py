"""
subset-to-gephi.py
Bart J - 2014-06-16.
This script generate a CSV that fits into Gephi
"""
import csv

# =====================================================================================
# Gephi Relationships
# =====================================================================================
fread = open('../data/PaperAuthor-subset.csv')
relationFwrite = open('../data/Gephi-relationships.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
relationWriter = csv.DictWriter(relationFwrite, delimiter=',', fieldnames=['Source','Target'])
relationWriter.writeheader()

for i,data in enumerate(reader):
	if data['PaperId'] and data['AuthorId']:
		relationWriter.writerow({'Source': 'p' + data['PaperId'], 'Target': 'a' + data['AuthorId']})

fread.close()

# =====================================================================================
# Gephi Nodes
# =====================================================================================
fread = open('../data/Author-subset.csv')
fwrite = open('../data/Gephi-nodes.csv','wb')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)
writer = csv.DictWriter(fwrite, delimiter=',', fieldnames=['Id','Name','Type'])
writer.writeheader()

for i,data in enumerate(reader):
	writer.writerow({'Id': 'a' + data['Id'], 'Name': data['Name'], 'Type': 'Author'})
fread.close()

fread = open('../data/Paper-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

for i,data in enumerate(reader):
	writer.writerow({'Id': 'p' + data['Id'], 'Name': data['Title'], 'Type': 'Paper'})

	#if data['ConferenceId']:
		#relationWriter.writerow({'Source': 'p' + data['Id'], 'Target': 'c' + data['ConferenceId']})
	#if data['JournalId']:
		#relationWriter.writerow({'Source': 'p' + data['Id'], 'Target': 'j' + data['JournalId']})

fread.close()

fread = open('../data/Conference-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

#for i,data in enumerate(reader):
#	writer.writerow({'Id': 'c' + data['Id'], 'Name': data['FullName'], 'Type': 'Venue'})
fread.close()

fread = open('../data/Journal-subset.csv')
reader = csv.DictReader(fread,delimiter=',', skipinitialspace=True)

#for i,data in enumerate(reader):
#	writer.writerow({'Id': 'j' + data['Id'], 'Name': data['FullName'], 'Type': 'Venue'})
fread.close()

fwrite.close()
relationFwrite.close()