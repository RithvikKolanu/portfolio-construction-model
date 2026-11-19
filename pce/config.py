from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WRDS_USERNAME = "rkolanu"

TICKERS = [
    "VTI", "EWC", "VGK", "VPL", "VWO",           # equities
    "IEF", "TLT", "BWX", "EMB",                  # government bonds
    "IGSB", "VCLT", "SJNK", "HYG", "PICB", "EUHY", "CEMB",  # credit
    "TIP", "VNQ", "VNQI", "IGF",                 # real assets
]
START, END = "2013-01-01", "2026-09-30"
OUT = ROOT / "data" / "returns.parquet"
MCAP_OUT = ROOT / "data" / "market_caps.parquet"
