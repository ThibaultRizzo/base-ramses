import yfinance as yf
data = yf.download("MSFT", start="2022-10-02", end="2022-10-06", interval = "1h", ignore_tz = False)
# data.index = data.index.map(lambda d: d.isoformat())
print(f"data {data}")
print('_______')
data = yf.download("TTE.PA", start="2022-10-02", end="2022-10-06", interval = "1h", ignore_tz = False)
# data.index = data.index.map(lambda d: d.isoformat())
print(f"data {data}")