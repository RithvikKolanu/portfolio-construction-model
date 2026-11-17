from sklearn.covariance import LedoitWolf
import numpy as np
import pandas as pd

def correlation(excess_returns):
    return excess_returns.corr()


def ledoit_wolf_covariance(excess_returns, periods_per_year = 52):
    X = ((excess_returns - excess_returns.mean(0)) / excess_returns.std()).to_numpy(dtype=float) # Standardize excess returns
    T, N = X.shape
    S = np.corrcoef(X, rowvar=False) # sample covariance matrix
    F = np.eye(N) * np.trace(S) / N # calculating mu * I
    d2 = ((S - F)**2).sum() 
    b2 = sum(((np.outer(x, x) - S) ** 2).sum() for x in X) / T**2
    delta = min(b2, d2) / d2

    shrunk = delta * F + (1-delta)*S

    cov = shrunk * np.outer(excess_returns.std(), excess_returns.std()) * periods_per_year # convert corr back to annualized cov
    return pd.DataFrame(cov, index=excess_returns.columns, columns=excess_returns.columns), delta
