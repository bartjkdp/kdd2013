from lib import GenerateFeatures
from lib import IO
from time import sleep
from itertools import izip
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

import sys
import evaluate

print '================================================================'
print 'KDD Cup 2013 - Track 1'
print 'Model by Bart Jeukendrup'
print '================================================================'
print 'Step 1/6: Reading CSV files to memory & pre-process data'
print '================================================================'

GenerateFeatures.authors = IO.readAuthors()
GenerateFeatures.venues = IO.readVenues()
GenerateFeatures.papers = IO.readPapers()
GenerateFeatures.authorpaper = IO.readAuthorPaper()
GenerateFeatures.paperauthor = IO.readPaperAuthor()

trainData = IO.readTrainData()
validData = IO.readValidData()

print '================================================================'
print 'Step 2/6: Generating features'
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
print 'Step 3/6: Training models'
print '================================================================'

rfClassifier = RandomForestClassifier(n_estimators=50, verbose=1, n_jobs=1, min_samples_split=10, random_state=1)
rfClassifier.fit(trainFeatures, trainLabels)

gbClassifier = GradientBoostingClassifier(n_estimators=100, verbose=1, learning_rate=1.0, max_depth=1, random_state=0)
gbClassifier.fit(trainFeatures, trainLabels)

print ''
print '================================================================'
print 'Step 4/6: Applying models'
print '================================================================'

rfPredictions = list(rfClassifier.predict_proba(validFeatures)[:,1])
gbPredictions = list(gbClassifier.predict_proba(validFeatures)[:,1])

print '================================================================'
print 'Step 5/6: Calculating ensemble'
print '================================================================'

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

sys.exit()