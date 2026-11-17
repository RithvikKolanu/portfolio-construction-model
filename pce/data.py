import pandas as pd
import wrds

from pce.config import TICKERS, START, END, OUT


def pull_returns():
    db = wrds.Connection()
    tickers = ", ".join(f"'{t}'" for t in TICKERS)

    ids = db.raw_sql(f"""
        select distinct on (ticker) ticker, permno
        from crsp.stksecurityinfohist
        where ticker in ({tickers})
        order by ticker, secinfoenddt desc
    """)
    missing = set(TICKERS) - set(ids["ticker"])
    assert not missing, f"not found in CRSP: {missing}"
    print(ids)

    permnos = ", ".join(str(int(p)) for p in ids["permno"])
    df = db.raw_sql(f"""
        select permno, dlycaldt as date, dlyret as ret
        from crsp.dsf_v2
        where permno in ({permnos}) and dlycaldt between '{START}' and '{END}'
    """, date_cols=["date"])

    rf = db.raw_sql(f"""
        select date, rf from ff.factors_daily
        where date between '{START}' and '{END}'
    """, date_cols=["date"])
    db.close()

    returns = df.pivot(index="date", columns="permno", values="ret")
    returns = returns.rename(columns=dict(zip(ids["permno"], ids["ticker"])))[TICKERS]
    returns["RF"] = rf.set_index("date")["rf"]

    OUT.parent.mkdir(exist_ok=True)
    returns.to_parquet(OUT)


def load_returns():
    if not OUT.exists():
        pull_returns()
    return pd.read_parquet(OUT).rename_axis(columns=None)
