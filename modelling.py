import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import statistics
import scipy

def correlation(xList, yList):
    """
    :param xList:
    :param yList:
    :return:
    """
    if len(xList) != len(yList):
        print('Lengths must be the same for both arrays')
    else:

        x_bar = sum(xList)/len(xList)
        y_bar = sum(yList)/len(yList)

        x_std = statistics.stdev(xList)
        y_std = statistics.stdev(yList)

        summation = 0
        for i in range(len(xList)):
            summation += ((xList[i] - x_bar)/x_std) * ((yList[i] - y_bar)/y_std)

        return (1/(len(xList)-1)) * summation


def mse(y, y_hat):
    return np.square(np.subtract(y,y_hat)).mean()

def predict(X, coefs, bias):
    return np.dot(X, coefs) + bias

def linear_regression(X, y): #still work in progress

    #initializing variables for iteration
    learning_rate = 0.01
    n_iterations = 1000
    coefs = np.zeros(X.shape[1])
    bias = 0
    loss = []


    #fitting with iteration
    for i in range(n_iterations):
        y_hat = np.dot(X, coefs) + bias
        error = mse(y, y_hat)
        loss.append(error)

        #finding adjustment differences
        partial_w = (1 / X.shape[0]) * (2 * np.dot(X.T, (y_hat - y)))
        partial_d = (1 / X.shape[0]) * (2 * np.sum(y_hat - y))

        #adjusting coefficient values
        coefs -= learning_rate * partial_w
        bias -= learning_rate * partial_d

    return coefs, bias


def ols(X, y):
    #coefficient list
    coefficients = []
    #constant initialization into matrix
    ones = np.ones(shape=X.shape[0]).reshape(-1,1)
    X = np.concatenate((ones, X), 1)

    #linear algebra solution fitting
    if len(X.shape) == 1:
        X = X.reshape(-1, 1)
    coefficients = np.linalg.inv(X.transpose().dot(X)).dot(X.transpose()).dot(y)

    bias = coefficients[0]
    coefs = coefficients[1:]

    return coefs, bias



class Model:
    def __init__(self, model, df, VOI, controls, resp, alpha = .05, interactions = None, IV_var = None, dummies = None):
        self.model = model
        self.df = df
        self.VOI = VOI
        self.controls = controls
        self.resp = resp
        self.alpha = alpha
        self.interactions = interactions
        self.IV_var = IV_var
        self.dummies = dummies

        #creating interaction terms
        interaction_labels = []
        if self.interactions is not None:
            for inter in self.interactions:
                self.df[f'{inter[0]}x{inter[1]}'] = self.df[inter[0]] * self.df[inter[1]]
                interaction_labels.append(f'{inter[0]}x{inter[1]}')

        #creating dummy variables
        dummy_labels = []
        if self.dummies is not None:
            for dum in self.dummies:
                for col in self.df:
                    if col == dum:
                        vals = list(set(self.df[col]))

                        for val in vals:
                            self.df[val] = [1 if x == val else 1 for x in self.df[col]]
                        dummy_labels.append(val)

        #creating feature matrix and response array
        feature_labels = [self.VOI] + controls + interaction_labels + dummy_labels
        feature_matrix = self.df[feature_labels].to_numpy()
        y = self.df[self.resp]



        #defining labels
        self.labels = feature_labels + [self.resp]

        #fitting linear regression
        if model == 'Linear':
            coefs, bias = linear_regression(feature_matrix, y)
            self.VOI_val = coefs[0]
            self.predict = predict(feature_matrix, coefs, bias)
            self.mse = mse(y, self.predict)
            self.r2 = 1 - self.mse/np.var(y)
            self.coefs = coefs
            self.bias = bias
        #fitting OLS
        if model == 'OLS':
            coefs, bias = ols(feature_matrix, y)
            self.VOI_val = coefs[0]
            self.constant = bias
            self.predict = predict(feature_matrix, coefs, bias)
            self.mse = mse(y, self.predict)
            self.r2 = 1 - self.mse/np.var(y)
            self.coefs = coefs
            self.bias = bias


    def __str__(self):
        return f'{self.model} model measuring effect of {self.VOI} on {self.resp}'


    # useful methods
    def corr_matrix(self):
        return self.df[self.labels].corr()

    def corr(self, var1, var2):
        return scipy.stats.pearsonr(self.df[var1], self.df[var2])[0]
        #return correlation(list(self.df[var1]), list(self.df[var2]))

    def plot_y_on_var(self, var, univariate = 'yes'):

        #plot data points
        plt.plot(self.df[var], self.df[self.resp], 'bo')


        #plot regression line if univariate == 'yes'
        if univariate == 'yes':
            coefs, bias = ols(self.df[[var]], self.df[self.resp])
            predictions = predict(self.df[[var]], coefs, bias)
            plt.plot(self.df[var], predictions)
        #plot regression line if univariate == 'no'
        else:
            plt.plot(self.df[var], self.predict)

        #formatting
        plt.title(f'Plot of {self.resp} on {var}')
        plt.ylabel(f'{self.resp}')
        plt.xlabel(f'{var}')
        plt.tight_layout()

    def residual_plot(self, var):
        sns.residplot(x = var, y = self.resp, data = self.df)
        plt.show()

        #formatting
        plt.title(f'Residual plot of residuals on predicted')
        plt.ylabel('Residuals')
        plt.xlabel('Predicted')
        plt.tight_layout()

    def pvalue(self, var):
        zeros = np.zeros(self.df[var].shape)
        return scipy.stats.ttest_ind(zeros, self.df[var])[1]
