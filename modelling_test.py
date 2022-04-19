import os
os.chdir(r'C:\Users\brend\Desktop\DS 5010\Project Phase 2')
import modelling

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math
import statistics





def main():
    data = sns.load_dataset('titanic').dropna()
    model = modelling.Model(model = 'OLS', df = data, VOI = 'fare', controls = ['pclass', 'survived'], resp = 'age')
    print('model coefficients: ', model.coefs, '\n \n')
    print('model variable of interest coefficient: ', model.VOI_val, '\n \n')
    print('model predictions: ', model.predict, '\n \n')
    print('model fare pvalue: ', model.pvalue('fare'), '\n \n')
    print('model correlation matrix: \n', model.corr_matrix(), '\n \n')
    print('model correlation between fare and age: ', model.corr('fare', 'age'), '\n \n')

    model.plot_y_on_var('fare')
    model.residual_plot('fare')

main()
