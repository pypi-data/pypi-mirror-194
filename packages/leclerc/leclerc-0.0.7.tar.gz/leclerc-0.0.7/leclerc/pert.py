# define a new class pertm_gen: a generator for the PERT distribution
# Based on tutorial at https://towardsdatascience.com/python-powered-monte-carlo-simulations-fc3c71b5b83f
# https://towardsdatascience.com/python-scenario-analysis-modeling-expert-estimates-with-the-beta-pert-distribution-22a5e90cfa79

import numpy as np
import matplotlib.pyplot as plt


from scipy.stats import qmc    # quasi-Monte Carlo for latin hypercube sampling
from scipy.stats import mstats 
from scipy import stats as stats
from scipy.stats import rv_continuous
import scipy.optimize as opt

from scipy.stats import norm, weibull_min, beta


import warnings
warnings.filterwarnings("ignore")


ksN = 100


class pertm_gen(rv_continuous):
    '''modified beta_PERT distribution'''
 
    def _shape(self, min, mode, max, lmb):
        s_alpha = 1+ lmb*(mode - min)/(max-min)
        s_beta = 1 + lmb*(max - mode)/(max-min)
        return [s_alpha, s_beta]


    def _cdf(self, x, min, mode, max, lmb):
        s_alpha, s_beta = self._shape(min, mode, max, lmb)
        z = (x - min) / (max - min)
        cdf = beta.cdf(z, s_alpha, s_beta)
        return cdf

    def _ppf(self, p, min, mode, max, lmb):
        s_alpha, s_beta = self._shape(min, mode, max, lmb)
        ppf = beta.ppf(p, s_alpha, s_beta)
        ppf = ppf * (max - min) + min
        return ppf


    def _mean(self, min, mode, max, lmb):
        mean = (min + lmb * mode + max) / (2 + lmb)
        return mean

    def _var(self, min, mode, max, lmb):
        mean = self._mean(min, mode, max, lmb)
        var = (mean - min) * (max - mean) / (lmb + 3)
        return var

    def _skew(self, min, mode, max, lmb):
        mean = self._mean(min, mode, max, lmb)
        skew1 = (min + max - 2*mean) / 4
        skew2 = (mean - min) * (max  - mean)
        skew2 = np.sqrt(7 / skew2)
        skew = skew1 * skew2
        return skew

    def _kurt(self, min, mode, max, lmb):
        a1,a2 = self._shape(min, mode, max, lmb)
        kurt1 = a1 + a2 +1
        kurt2 = 2 * (a1 + a2)**2
        kurt3 = a1 * a2 * (a1 + a2 - 6)
        kurt4 = a1 * a2 * (a1 + a2 + 2) * (a1 + a2 + 3)
        kurt5 = 3 * kurt1 * (kurt2 + kurt3)
        kurt = kurt5 / kurt4 -  3                 # scipy defines kurtosis of std normal distribution as 0 instead of 3
        return kurt

    def _stats(self, min, mode, max, lmb):
        mean = self._mean(min, mode, max, lmb)
        var = self._var(min, mode, max, lmb)
        skew = self._skew(min, mode, max, lmb)
        kurt = self._kurt(min, mode, max, lmb)
        return mean, var, skew, kurt

if __name__ == "__main__":
    print("Running")

    min, mode, max, lmb = 8000.0, 12000.0, 18000.0, 4.0


    # instantiate a PERT object and print stats
    pertm = pertm_gen(name="pertm")
    rvP = pertm(min,mode,max,lmb)
    statsP = rvP.stats("mvsk")

    moments = [np.asscalar(v) for v in statsP]
    moment_names = ["mean", "var", "skew", "kurt"]
    dict_moments = dict(zip(moment_names, moments))
    _ = [print(k,":",f'{v:.2f}') for k,v in dict_moments.items()]

    # Draw histogram of random samples
    N = 10000
    sampler01 = qmc.LatinHypercube(d=1, seed=42)    # d = dimension
    sample01 = sampler01.random(n=N)
    # Generate array of random samples from the distribution
    randP = rvP.ppf(sample01)
    print(randP)

    fig, ax = plt.subplots(1, 1)
    ax.hist(randP, density=True, histtype='stepfilled', alpha=0.2)
    ax.legend(loc='best', frameon=False)
    plt.show()
    pass
