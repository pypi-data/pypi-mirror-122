"""
Implementation of the Logistic Regression Algorithm
"""
import numpy as np
import pandas as pd 

from numpy.core.fromnumeric import var
from numpy.linalg import pinv
import pandas as pd
import numpy as np

"""
Helper functions to help in data manipulation
"""

"""
Functions to generate different plots
"""

import matplotlib.pyplot as plt 
import seaborn as sns 

"""
Basic Scatter Plot
"""
def generateScatterPlot(x,y):
    plt.scatter(x,y)
    plt.show()


"""
Basic Box Plot
"""
def generateBoxPlot(x,figSize):
    plt.figure(figsize=figSize)
    sns.boxplot(x)
    plt.show()

"""
Basic Histogram
"""
def generateHistogram(x,y):
    plt.hist(x,y)
    plt.show()

"""
Basic Correlation Matrix
"""
def generateCorrelationMatrix(data):
    corr = data.corr()
    corr.style.background_gradient()
    return corr

"""
Pandas implementation of train_test_split
Note: Should be split into Features and Labels post split
"""

def getTrainingTestingData(data, trainingRatio = 0.75, seed = 42):

    # Step 1
    trainingData = data.sample(frac = trainingRatio, random_state = seed)

    # Step 2 
    trainingIndex = trainingData.index 

    # Step 3 
    testingData = data.drop(trainingIndex)

    return trainingData,testingData

"""
Sigmoid Function
"""
def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

"""
Append a number to the start of every row in a matrix
"""
def appendNumberToEveryRow(array,number):
    return np.insert(array,0,number,axis=1)

"""
Reshaping a Matrix array to newDimensions
"""
def reshapeVector(array,newDimensions):
    return np.reshape(array,newDimensions)

"""
Get Error Metrics of the Model
"""
def getErrorMetrics(x,weights,y):
    predictedY = np.dot(x,weights)
    probabilityValues = sigmoid(predictedY)
    
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for i in range(len(probabilityValues)):
        if probabilityValues[i] >= 0.5 and y[i] == 1:
            tp += 1
        elif probabilityValues[i] < 0.5 and y[i] == 0:
            tn += 1 
        elif probabilityValues[i] >= 0.5 and y[i] == 0:
            fp += 1 
        else:
            fn += 1 

    accuracyDict = {}
    accuracyDict["accuracy"] = (tp+tn)/(tp+tn+fp+fn)
    accuracyDict["tp"] = tp 
    accuracyDict["tn"] = tn 
    accuracyDict["fp"] = fp
    accuracyDict["fn"] = fn 
    return accuracyDict 

"""
Parse a Pandas DataFrame to a Numpy Array
"""
def dataFrameToNumpyArray(dataFrame):
    return dataFrame.to_numpy()

"""
Compute the Gaussian Probability
"""
def getGaussianLogVector(x,mean,sigma):
    const = -x.shape[1] / 2 * np.log(2 * np.pi) - 0.5 * np.sum(np.log(sigma))
    probs = 0.5 * np.sum(np.power(x - mean, 2) / (sigma), 1)
    return const - probs
    

"""
Get the mean over an array with column Calculation Index colIndex
"""
def getMeanOverArray(array, colIndex):
    return np.mean(array,axis = colIndex)

"""
Get the variance over an array with column Calculation Index colIndex
"""
def getVarianceOverArray(array, colIndex):
    return np.var(array, axis = colIndex)

"""
Return the Index of the Maximum Value of Array along axis colIndex
"""
def getMaximumIndex(array, colIndex):
    return np.argmax(array, axis = colIndex)

"""
Return the Inverse of a Matrix
"""
def getMatrixInverse(x):
    return pinv(x)




"""
Implementation of the Logistic Regression Algorithm
"""
class LogisticRegression:

    """
    Constructor
    """
    def __init__(self,x,y):
        self._x = np.array(x,dtype='float') 
        self._y = np.array(y,dtype='float') 
        self._numRecords = self._x.shape[0]

    """
    Gradient Descent Solution
    """
    def getParametersGradientDescent(self,learningRate = 0.00001,numInterations = 1000,decay = 0):
        # Converting the input into suitable shapes
        x = appendNumberToEveryRow(self._x,1)
        y = reshapeVector(self._y,(self._numRecords,1))
        n = self._numRecords
        
        # Performing the computation
        numFeatures = x.shape[1]
        weights = np.zeros((numFeatures,1))

        for _ in range(numInterations):

            # Step 1
            calc1 = np.dot(x,weights)

            # Step 2
            calc2 = sigmoid(calc1)

            # Step 3 
            calc3 = np.dot(x.T, (y - calc2))

            # Step 4 
            weights += (1.0/n) * learningRate * calc3 

            # Step 5 
            learningRate -= decay
        
        return weights
        

    """
    Get Solution for Logistic Regression using Newton's Method
    """
    def getNewtonMethodSolution(self, numIterations = 1000):
        # Converting the input into suitable shapes
        x = appendNumberToEveryRow(self._x,1)
        y = reshapeVector(self._y,(self._numRecords,1))
        n = self._numRecords

        # Performing the computation
        numFeatures = x.shape[1]
        weights = np.zeros((numFeatures,1))

        for _ in range(numIterations):

          calc1 = np.dot(x,weights)

          calc2 = sigmoid(calc1)

          calc3 = (1.0/n) * np.dot(x.T, (calc2 - y))

          temp1 = calc2.reshape(n,)
          temp2 = np.diag(temp1)

          temp3 = (1-calc2).reshape(n,)
          temp4 = np.diag(temp3)

          calc4 = (1.0/n) * (x.T.dot(temp2)).dot(temp4).dot(x)

          weights -= getMatrixInverse(calc4).dot(calc3)
        
        return weights


    """
    Get Training Accuracy
    """
    def getAccuracy(self,weights):
        x = appendNumberToEveryRow(self._x,1)
        y = reshapeVector(self._y,(self._numRecords,1))
        return getErrorMetrics(x,weights,y)
    
    """
    Get Testing Accuracy
    """
    def getTestingAccuracy(self,x,y,weights):
        x = np.array(x)
        y = np.array(y)
        x = appendNumberToEveryRow(x,1)
        y = reshapeVector(y,(x.shape[0],1))
        return getErrorMetrics(x,weights,y)