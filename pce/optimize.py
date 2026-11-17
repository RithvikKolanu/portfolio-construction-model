import cvxpy as cp
import numpy as np
import pandas as pd

def min_variance(Sigma, max_weight = 1):
    w = cp.variable(len(Sigma))
    cp.Problem(
        cp.Minimize(cp.quad_form(w, Sigma.to_numpy(dtype=float))),
        [cp.sum(w) == 1, w >= 0, w <= max_weight]
    ).solve()
    return pd.Series(w.value, index = Sigma.index)