from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TICKERS = [
    "VTI", "EWC", "VGK", "VPL", "VWO",           # equities
    "SHY", "IEF", "TLT", "BWX", "EMB",           # government bonds
    "IGSB", "VCLT", "SJNK", "HYG", "PICB", "EUHY", "CEMB",  # credit
    "TIP", "VNQ", "VNQI", "GLD", "IGF", "DBC",   # real assets
]
START, END = "2013-01-01", "2026-09-30"
OUT = ROOT / "data" / "returns.parquet"
