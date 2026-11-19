import pandas as pd

VIEWS = [
    # J.P. Morgan 2027 LTCMA (Oct 2026), anchored on intermediate Treasuries at 4.6%
    ({"VTI": 1, "IEF": -1}, 0.075 - 0.046, "JPM: US large cap 7.5% vs int. Treasuries 4.6%"),
    ({"VWO": 1, "IEF": -1}, 0.071 - 0.046, "JPM: EM equity 7.1% vs int. Treasuries 4.6%"),
    ({"IGSB": 0.5, "VCLT": 0.5, "IEF": -1}, 0.061 - 0.046, "JPM: US IG credit 6.1% vs int. Treasuries 4.6%"),
    ({"HYG": 1, "IEF": -1}, 0.067 - 0.046, "JPM: US high yield 6.7% vs int. Treasuries 4.6%"),

    # Vanguard 10y forecasts (Sep 30 2026), range midpoints
    ({"VGK": 1/3, "VPL": 1/3, "EWC": 1/3, "VTI": -1}, 0.063 - 0.058, "Vanguard: dev. ex-US equity 6.3% vs US equity 5.8%"),
    ({"VWO": 1, "VTI": -1}, 0.047 - 0.058, "Vanguard: EM equity 4.7% vs US equity 5.8%"),
    ({"EMB": 1, "HYG": -1}, 0.069 - 0.059, "Vanguard: EM sovereign 6.9% vs US high yield 5.9%"),
]


def views_to_PQ(tickers):
    P = pd.DataFrame([w for w, _, _ in VIEWS], columns=tickers).fillna(0.0)
    P.index = [s for _, _, s in VIEWS]
    Q = pd.Series([q for _, q, _ in VIEWS], index=P.index)
    return P, Q
