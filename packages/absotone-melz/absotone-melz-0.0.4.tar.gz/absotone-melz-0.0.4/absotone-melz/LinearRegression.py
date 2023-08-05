import numpy as np
import pandas as pd 

import numpy as np
import pandas as pd 

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
Get Modulus of a given value
"""
def mod(x):
    if x >= 0:
        return x 
    else:
        return -x

"""
Get RMSE error of Regression
"""
def getMeanSquaredError(given_data,weights,test_data):
    n = given_data.shape[0]

    # Performing the calculation
    errorValue = 0

    # Step 1 
    calc1 = np.dot(given_data,weights)

    # Step 2
    for i in range(n):
        errorValue += np.power(calc1[i]-test_data[i],2)/float(n)
    
    return errorValue

"""
Parse a Pandas DataFrame to a Numpy Array
"""
def dataFrameToNumpyArray(dataFrame):
    return dataFrame.to_numpy()
 

"""
Append a fixed number to the start of every row in a matrix
"""
def appendNumberToEveryRow(array,number):
    return np.insert(array,0,number,axis=1)

"""
Reshape a given array to newDimensions.
"""
def reshapeVector(array,newDimensions):
    return np.reshape(array,newDimensions)

"""
Get MARE value of Regression.
"""
def getMeanAbsoluteError(given_data,weights,test_data):
    n = given_data.shape[0]

    # Performing the calculation
    errorValue = 0

    # Step 1 
    calc1 = np.dot(given_data,weights)

    # Step 2
    for i in range(n):
        errorValue += mod(calc1[i] - test_data[i])/float(n)
    
    return errorValue




"""
Implementation of Multivariate Linear Regression
"""
class LinearRegression:
    """
    Constructor
    """
    def __init__(self,x,y):
        self._x = np.array(x,dtype='float') 
        self._y = np.array(y,dtype='float') 
        self._numRecords = self._x.shape[0]

    """
    Closed Form Solution
    """
    def getParametersClosedForm(self):
        # Converting the input into suitable shapes
        x = appendNumberToEveryRow(self._x,1)
        y = reshapeVector(self._y,(self._numRecords,1))


        # Step 1
        calc1 = np.dot(x.T,x)
        calc2 = np.linalg.inv(calc1)

        # Step 2
        calc3 = np.dot(calc2,x.T)

        #Step 3
        weights = np.dot(calc3,y)

        return weights


    """
    Gradient Descent Solution
    """
    def getParametersGradientDescent(self,learningRate = 0.00001,numInterations = 1000,decay = 0):
        # Converting the input into suitable shapes
        x = appendNumberToEveryRow(self._x,1)
        y = reshapeVector(self._y,(self._numRecords,1))
        weights = np.zeros((self._x.shape[1]+1,1))

        # Performing the calculation
        n = self._numRecords

        for _ in range(numInterations):

            # Step 1 
            calc1 = np.dot(x,weights)

            # Step 2 
            calc2 = (2.0/n) * np.dot(x.T,calc1-y)

            # Step 3 
            weights = weights - learningRate*calc2 

            # Step 4 
            learningRate -= decay
        
        return weights
    
    """
    Newton's Method Solution
    """
    def getParametersNewtonMethod(self,numIterations):
        pass 

    
    """
    Get Combined Accuracy
    """
    def getAccuracyTraining(self, weights):
        # Converting the input into suitable shapes
        x = appendNumberToEveryRow(self._x, 1)
        y = self._y 

        rmseError = getMeanSquaredError(x,weights,y)
        mareError = getMeanAbsoluteError(x,weights,y)

        accuracyDict = {
            "MeanSquaredError" : rmseError,
            "MeanAbsoluteError" : mareError
        }

        return accuracyDict

    """
    Get Accuracy of Test Data
    """
    def getAccuracyTesting(self,x,y,weights):
        
        # Converting the input into suitable shapes
        x = np.array(x)
        y = np.array(y)

        x = appendNumberToEveryRow(x,1)
        y = reshapeVector(y,(x.shape[0],1))

        # Performing the calculation
        rmseError = getMeanSquaredError(x,weights,y)
        mareError = getMeanAbsoluteError(x,weights,y)

        accuracyDict = {
            "MeanSquaredError" : rmseError,
            "MeanAbsoluteError" : mareError
        }

        return accuracyDict





    
