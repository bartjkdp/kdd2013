"""
model.py
Bart J - 2014-06-01.
KDD Cup 2013 Track 1
"""
from __future__ import division
from lib import IO
from lib import PreProcess
from lib import InitialCalculation
from lib import GenerateFeatures
from time import sleep
from itertools import izip
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity

import sys
import evaluate
import __builtin__

def Step1():
	print '================================================================'
	print 'KDD Cup 2013 - Track 1'
	print 'Model by Bart Jeukendrup'
	print '================================================================'
	print 'Step 1/6: Reading CSV files to memory & pre-process data'
	print '================================================================'

	# Read all the data from the files or the memory cache
	IO.readAuthors()
	IO.readVenues()
	IO.readPapers()
	IO.readAuthorPaper()

	IO.readTrainData()
	IO.readValidData()

	# Preprocess string values (strip HTML, lower, character encoding)
	__builtin__.authors = PreProcess.authors(__builtin__.authors)
	__builtin__.papers = PreProcess.papers(__builtin__.papers)
	__builtin__.venues = PreProcess.venues(__builtin__.venues)
	_builtin__.paperauthor = PreProcess.paperauthors(__builtin__.paperauthor)

	print '================================================================'
	print 'Step 2/6: Initial feature calculation'
	print '================================================================'

	# Calculate adjecency and probability matrixes of HeteSim
	InitialCalculation.calculate()

def Step2():
	print '================================================================'
	print 'Step 3/6: Generating features'
	print '================================================================'

	trainLabels = []
	trainFeatures = []
	validFeatures = []

	print 'Generating features for train data...'

	for trainRow in trainData:
		trainLabels.append(trainRow['label'])
		trainFeatures.append(GenerateFeatures.allFeatures(trainRow['authorId'], trainRow['paperId']))

	print 'Generating features for validation data...'
	for validRow in validData:
		validFeatures.append(GenerateFeatures.allFeatures(validRow['authorId'], validRow['paperId']))

	print '================================================================'
	print 'Step 4/6: Training models'
	print '================================================================'

	rfClassifier = RandomForestClassifier(n_estimators=100, verbose=1, n_jobs=-1, min_samples_split=10, random_state=1)
	rfClassifier.fit(trainFeatures, trainLabels)

	gbClassifier = GradientBoostingClassifier(n_estimators=100, verbose=1, learning_rate=1.0, max_depth=3, random_state=0)
	gbClassifier.fit(trainFeatures, trainLabels)

	print '================================================================'
	print 'Step 5/6: Applying models'
	print '================================================================'

	rfPredictions = list(rfClassifier.predict_proba(validFeatures)[:,1])
	gbPredictions = list(gbClassifier.predict_proba(validFeatures)[:,1])

	print 'Taking the weighted average of the two models'
	predictions = []
	for prediction in zip(rfPredictions, gbPredictions):
		# Take the weighted average of the two models
		predictions.append(0.5 * prediction[0] + 0.5 * prediction[1])

	print '================================================================'
	print 'Step 6/6: Saving results and calculate performance'
	print '================================================================'

	IO.writePredictions(predictions, validData)
	evaluate.calculate_map()

if __name__ == "__main__":
	Step1()
	Step2()
