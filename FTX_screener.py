import client
import pandas as pd
import numpy as np
from datetime import datetime as dt

API_KEY =
API_SECRET =

ftx = client.FtxClient(api_key=API_KEY, api_secret=API_SECRET)

def get_top10(n = 10):
    futures = pd.DataFrame(ftx.get_all_futures())
    futures['expiry'] = pd.to_datetime(futures['expiry']).dt.tz_localize(None)
    df = futures[futures["type"]=="future"][["bid", "ask", "mark", "index", "expiry"]]
    df = df[(df["ask"]-df["bid"])/df["ask"] < 0.01 ] #"pessimistic" approach, we get filled @ask
    futures["basis"] = df["ask"] - df["index"]
    futures["% basis PA"] = (futures["basis"] / df["index"]) * (365 / (df["expiry"] - np.datetime64('today')).dt.days) * 100
    top = futures.nlargest(n, ["% basis PA"])[["name", "% basis PA", "mark", "index", "description"]]
    return top

print(get_top10())
