import IO
import jellyfish
	
	
def allFeatures(authorId, paperId):
	features = []

	features.append(jaroWinklerDistanceAuthorPaper(authorId, paperId))
	features.append(jaroWinklerDistanceAffiliation(authorId, paperId))

	return features

def jaroWinklerDistanceAuthorPaper(authorId, paperId):
	global authors
	global paperauthor
		
	if authors[authorId]['name'] and paperauthor[paperId][authorId]['authorName']:
		return jellyfish.jaro_distance(authors[authorId]['name'], 
								       paperauthor[paperId][authorId]['authorName'])
	else:
		return 0.5
		
def jaroWinklerDistanceAffiliation(authorId, paperId):
	global authors
	global paperauthor
	
	if authors[authorId]['name'] and paperauthor[paperId][authorId]['authorName']:
		return jellyfish.jaro_distance(authors[authorId]['affiliation'], 
								       paperauthor[paperId][authorId]['affiliation'])
	else:
		return 0.5