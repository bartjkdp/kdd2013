import csv
import numpy as np
from collections import OrderedDict

def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average prescision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The average precision at k over the input lists

    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 1.0

    return score / min(len(actual), k)


def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.

    This function computes the mean average prescision at k between two lists
    of lists of items.

    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted 
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The mean average precision at k over the input lists

    """
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])

def calculate_map():
	# Read predictions
	f = open('data/ValidPredicted.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)

	predictions = []
	for i,data in enumerate(reader):
		predictions.append(data['PaperIds'].split())
	f.close()

	# Read actual solutions
	f = open('data/ValidSolution.csv')
	reader = csv.DictReader(f,delimiter=',', skipinitialspace=True)

	actuals = []
	for i,data in enumerate(reader):
		actuals.append(data['PaperIds'].split())
	f.close()

	# Calculate MAP
	result = mapk(actuals, predictions, 10000)
	print "Mean Average Precision: ", result
	return result

if __name__=="__main__":
	calculate_map()