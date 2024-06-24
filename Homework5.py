# -*- coding: utf-8 -*-
"""Elec378HW5.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19_-DdLmA6K2vXA64UpQrV5sAATJpdp4J
"""

import sklearn
from keras.datasets import mnist
from sklearn.linear_model import LogisticRegression
import numpy as np
from matplotlib import pyplot as plt
from sklearn.datasets import load_digits
from scipy.spatial.distance import cdist
from scipy.stats import mode
from sklearn.model_selection import train_test_split

digits = load_digits()

X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=0)
index = 100

plt.imshow(X_train[index].reshape((8,8)))
print(f'Digit: {y_train[index]}')

def knn(X_fit, y_fit, X_predict, n_neighbors=5, metric='euclidean'):
    '''
    inputs:
        X_fit - 2D array containing all training data points
        y_fit - 2D array containing all training data labels
        X_predict - 2D array containing all data points to classify
        n_neighbors - K
        metric - see scipy.spatial.distance.cdist:
                 https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cdist.html

    returns: a 1D array of predicted labels for X_predict.
    '''

    # Make sure that X_predict is two dimensional.
    # This only matters if X_predict is one data point.
    if X_predict.ndim < 2:
        X_predict = [X_predict]

    # Calculate distances
    distances = cdist(X_predict, X_fit, metric)

    # Find the data indices of least distance for each point.
    # Keep the closest n_neighbors data points for each point.
    closest = np.argsort(distances, axis=1)[:,:n_neighbors]

    # Find the label of the n_neighbors closest data points
    closest_labels = y_fit[closest]

    '''
    Get the mode of each row. Return the resulting 1-D array of labels.
    See the docs for more information concerning the array slicing:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mode.html
    '''
    return mode(closest_labels, axis=1)[0]

error_rates = {'euclidean': [], 'cityblock': [], 'chebyshev': []}
ks = range(1, 15)

for metric in error_rates.keys():
    for K in ks:
        predictions = knn(X_fit=X_train, y_fit=y_train, X_predict=X_test, n_neighbors=K, metric=metric)
        error = np.count_nonzero(predictions.flatten() != y_test) / np.size(y_test)
        error_rates[metric].append(error)

for metric, errors in error_rates.items():
    plt.plot(ks, errors, label=metric)

plt.xlabel('Number of Neighbors K')
plt.ylabel('Misclassification Error')
plt.title('Error vs K for Different Distance Metrics')
plt.legend()
plt.show()

"""Euclidean = 2-norm

Cityblock = 1-norm

Chebyshev = $\infty$-norm

Comparing the 1-norm to the 2-norm, the 2-norm generally has a lower misclassification rate than the 1-norm. Both have the lowest misclassificiation rate with K=1, and trend in the direction of increasing error as K increases.


Comparing the $\infty$-norm to the 1-norm, the $\infty$-norm generally has a lower misclassification rate than the 1-norm. While the 1-norm has the lowest misclassification rate at K=1, the $\infty$-norm has the lowest misclassification rate at K=1 and K=3. Both trend in the direction of increasing error as K increases.

Comparing the $\infty$-norm to the 2-norm, the two alternate which has the lower misclassification rate as K increases. The 2-norm has the lowest misclassification rate at K=1 and the $\infty$-norm has the lowest misclassification rate at K=1 and K=3.

The error between the different metrics has a smaller magnitude than the error between different values of K.

"""
