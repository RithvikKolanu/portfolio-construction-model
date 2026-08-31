import wrds
db = wrds.Connection(wrds_username="rkolanu")

import os, hashlib, time
from datetime import date
import pandas as pd

CACHE_DIR = "cache"

def fetch_etf_permnos(db, tickers):
    etf_list = db.raw_sql(
        "SELECT DISTINCT ON (permno) permno, ticker, comnam, nameenddt "
        "FROM crsp.stocknames WHERE shrcd = 73 "
        "ORDER BY permno, nameenddt DESC",
        date_cols=["nameenddt"],
    )
    return etf_list[etf_list["ticker"].isin(tickers)][["permno", "ticker"]]


def cached_pull(db, universe, start, end, max_age_days=1):
    picks = fetch_etf_permnos(db, universe)         
    permnos = picks["permno"].tolist()
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = hashlib.md5(
        ("|".join(map(str, sorted(permnos))) + start + end).encode()
    ).hexdigest()[:10]
    path = os.path.join(CACHE_DIR, f"crsp_{key}.parquet")

    # fresh cache hit -> no WRDS call at all
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < max_age_days * 86400:
        return pd.read_parquet(path)

    data = db.raw_sql(
        "SELECT permno, date, ret, prc, vol FROM crsp.dsf "
        "WHERE permno IN %(permnos)s AND date BETWEEN %(start)s AND %(end)s "
        "ORDER BY permno, date",
        params={"permnos": tuple(permnos), "start": start, "end": end},
        date_cols=["date"],
    )
    data = data.merge(picks, on="permno")
    if not data.empty:
        data.to_parquet(path)        # save for next run
    return data

universe = [
    "SPY", "EWC", "EFA", "EEM",        # equity core
    "SHY", "IEF", "TLT",               # govt duration ladder
    "TIP",                             # real return
    "LQD", "HYG",                      # credit
    "VNQ", "GLD", "IGF",               # real assets
]
START, END = "2010-01-01", date.today().isoformat()

data = cached_pull(db, universe, START, END)
rets = (data.pivot(index="date", columns="ticker", values="ret"))
print(rets)