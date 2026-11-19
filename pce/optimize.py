import cvxpy as cp
import numpy as np
import pandas as pd

def min_variance(Sigma, max_weight = 1, mu = None, target_return = None):
    w = cp.Variable(len(Sigma))
    constraints = [cp.sum(w) == 1, w >= 0, w <= max_weight]
    if target_return is not None:
        constraints.append(mu.values @ w >= target_return)
    problem = cp.Problem(
        cp.Minimize(cp.quad_form(w, Sigma.to_numpy(dtype=float))),
        constraints
    )
    problem.solve(solver=cp.CLARABEL)
    if problem.status != "optimal":
        raise ValueError(f"No portfolio reaches {target_return:.2%} under these constraints")
    return pd.Series(w.value, index=Sigma.index), problem.value

def black_litterman(Sigma, w_mkt, P = None, Q = None, delta = 2.5, tau = 0.05, max_weight = 1):
    S = Sigma.to_numpy(dtype=float)
    pi = delta * S @ w_mkt.to_numpy(dtype=float)  # implied equilibrium excess returns

    if P is None:
        mu = pi
    else:
        P, Q = np.asarray(P, dtype=float), np.asarray(Q, dtype=float)
        Omega = np.diag(np.diag(P @ (tau * S) @ P.T))  # view uncertainty proportional to prior variance
        A = np.linalg.inv(tau * S)
        mu = np.linalg.solve(A + P.T @ np.linalg.inv(Omega) @ P, A @ pi + P.T @ np.linalg.inv(Omega) @ Q)

    w = cp.Variable(len(Sigma))
    problem = cp.Problem(
        cp.Maximize(mu @ w - delta / 2 * cp.quad_form(w, S)),
        [cp.sum(w) == 1, w >= 0, w <= max_weight]
    )
    problem.solve(solver=cp.CLARABEL)
    return pd.Series(w.value, index=Sigma.index), pd.Series(mu, index=Sigma.index)
