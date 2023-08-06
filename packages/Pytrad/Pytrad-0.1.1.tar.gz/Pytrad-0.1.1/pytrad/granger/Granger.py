import os, sys
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(BASE_DIR)
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests
from sklearn.linear_model import LassoCV


class Granger(object):
    def __init__(self, maxlag=2):
        self.maxlag = maxlag

    def granger_test(self, data, test='ssr_ftest'):
        n, dim = data.shape
        p_value_matrix = np.zeros((dim, dim))
        for c in range(dim):
            for r in range(dim):
                test_result = grangercausalitytests(data[:, [r, c]], maxlag=self.maxlag, verbose=False)
                p_values = [round(test_result[i + 1][0][test][1], 4) for i in range(self.maxlag)]
                min_p_value = np.min(p_values)
                p_value_matrix[r, c] = min_p_value
        return p_value_matrix

    def granger_lasso(self, data, cv=5):

        n, dim = data.shape
        # stack data to form one-vs-all regression
        Y = data[self.maxlag:]
        X = np.hstack([data[self.maxlag-k:-k] for k in range(1, self.maxlag+1)])

        lasso_cv = LassoCV(cv=cv)
        coeff = np.zeros((dim, dim*self.maxlag))
        # Consider one variable after the other as target
        for i in range(dim):
            lasso_cv.fit(X, Y[:,i])
            coeff[i] = lasso_cv.coef_
        return coeff