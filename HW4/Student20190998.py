#i/usr/bin/python3

import sys
import numpy as np
import operator
from os import listdir

test = sys.argv[2]
train = sys.argv[1]
testDigits = listdir(test)
trainDigits = listdir(train)

def FileToVector(fName):
	vector = np.zeros((1, 1024))

	with open(fName) as f:
		for i in range(32):
			line = f.readline()

			for j in range(32):
				vector[0, 32 * i + j] = int(line[j])

	return vector

def createDataSet(dataset):
	m = len(trainDigits)
	group = np.zeros((m, 1024))
	labels = []

	for i in range(m):
		fName = trainDigits[i]
		answer = int(fName.split('_')[0])
		labels.append(answer)
		group[i, :] = FileToVector(dataset + '/' + fName)

	return group, labels

def classify0(inX, dataset, labels, k):
	datasetSize = dataset.shape[0]
	diffMat = np.tile(inX, (datasetSize, 1)) - dataset
	sqDiffMat = diffMat ** 2
	sqDistances = sqDiffMat.sum(axis = 1)
	distances = sqDistances ** 0.5
	sortedDistIndicies = distances.argsort()
	classCount = {}

	for i in range(k):
		voteIlabel = labels[sortedDistIndicies[i]]
		classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
	sortedClassCount = sorted(classCount.items(), key = operator.itemgetter(1), reverse = True)
	
	return sortedClassCount[0][0]

group, labels = createDataSet(train)

for k in range(1, 21):
	count = 0
	fail = 0

	for i in range(len(testDigits)):
		testData = FileToVector(test + '/' + testDigits[i])
		answer = int(testDigits[i].split('_')[0])
		expect = classify0(testData, group, labels, k)

		if answer != expect:
			fail += 1
		count += 1
	result = int((fail / count) * 100)
	
	print(result)
