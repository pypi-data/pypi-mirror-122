import os, sys
BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(BASE_DIR)
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, WhiteKernel, ConstantKernel as C
from pytrad.utils.KCI.KCI import KCI_UInd
from pytrad.utils.KCI import GaussianKernel


class ANM(object):
    def __init__(self, maxlag=2):
        self.maxlag = maxlag

    def fit_gp(self, X, y):
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2)) + WhiteKernel(0.1, (1e-10, 1e+1))
        gpr = GaussianProcessRegressor(kernel=kernel)

        # fit Gaussian process, including hyperparameter optimization
        gpr.fit(X, y)
        pred_y = gpr.predict(X)
        return pred_y

    def cause_or_effect(self, data_x, data_y):
        N = data_x.shape[0]
        # set up unconditional test
        kernelX = GaussianKernel()
        kernelY = GaussianKernel()
        kci = KCI_UInd(N, kernelX, kernelY)

        # test x->y
        pred_y = self.fit_gp(data_x, data_y)
        res_y = data_y - pred_y
        pval_foward, _ = kci.compute_pvalue(data_x, res_y)

        # test y->x
        pred_x = self.fit_gp(data_y, data_x)
        res_x = data_x - pred_x
        pval_backward, _ = kci.compute_pvalue(data_y, res_x)

        return pval_foward, pval_backward