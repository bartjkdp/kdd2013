import IO
import jellyfish
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer	
from sklearn.metrics.pairwise import cosine_similarity
	
def allFeatures(authorId, paperId):
	features = []

	features.append(jaroWinklerDistanceAuthorPaper(authorId, paperId))
	features.append(jaroWinklerDistanceAffiliation(authorId, paperId))
	#features.append(tfidfPaperAuthorPapers(authorId, paperId))

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

authorTfidfVectorizer = {}
def tfidfPaperAuthorPapers(authorId, paperId):
	global papers
	global authorpaper
	global authorTfidf
	
	# Cache vectorizer for speed improvement
	if authorId not in authorTfidfVectorizer:
		stopwords = nltk.corpus.stopwords.words('english')
		vectorizer = TfidfVectorizer(stop_words = stopwords, min_df=1)
		
		analyse = []
		for paper in authorpaper[authorId]:
			analyse.append(papers[paper]['title'] + ' ' + papers[paper]['keywords'])
		
		vectorizer.fit_transform(analyse)
		authorTfidfVectorizer[authorId] = vectorizer
		
	vectorizer = authorTfidfVectorizer[authorId]
	
	analyse = []
	for paper in authorpaper[authorId]:
		analyse.append(papers[paper]['title'] + ' ' + papers[paper]['keywords'])

	currentAuthorPapers = vectorizer.transform(analyse)
	currentPaper = vectorizer.transform([papers[paperId]['title'] + ' ' + papers[paperId]['keywords']])
	
	cosSim = 0
	i = 0
	
	for currentAuthorPaper in currentAuthorPapers:
		cosSim = cosSim + float(cosine_similarity(currentPaper, currentAuthorPaper))
		i = i + 1
		
	return cosSim/i