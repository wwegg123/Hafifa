from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import pandas as pd
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()

DST_PATH = os.getenv('DST_PATH')

TICKER_BTC = os.getenv('TICKER_BTC')
TICKER_GOOG = os.getenv('TICKER_GOOG')
TICKER_AMZN = os.getenv('TICKER_AMZN')

TRACKED_STOCKS = {
    TICKER_BTC:os.getenv('BTC_HOURS'),
    TICKER_GOOG:os.getenv('GOOG_HOURS'),
    TICKER_AMZN:os.getenv('AMZN_HOURS')
}

def get_coin_data(ticker, dates):
    data = yf.download(
        ticker,
        start= min(dates) - timedelta(days=1),
        end= max(dates) + timedelta(days=1),
        interval="1h",
        progress=False
    )
    
    data.index = data.index.tz_convert("UTC")
    data = data.loc[
        data.index.strftime("%Y-%m-%d %H").isin(
            dates.strftime("%Y-%m-%d %H")
        )
    ]

    data["Pct Change"] = data["Close"].pct_change() * 100

    result = pd.DataFrame({
        "Hour": data.index,
        "Stock Type": ticker,
        "Percentage Change": data["Pct Change"]
    })
    return result

def save_coin_data(dst_path, data):
    data.to_csv(dst_path)

def hour_rounder(time):
    return (time.replace(second=0, microsecond=0, minute=0, hour=time.hour)
               +timedelta(hours=time.minute//30))

def read_dates(hours_path):
    dates = []

    with open(hours_path, 'r') as dates_file:
        for date in dates_file:
            dates.append((
                datetime.strptime(date.strip(), "%Y-%m-%d %H:%M:%S.%f")))
            
    dates = pd.to_datetime(dates, utc=True)
    return dates

if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for ticker, path in TRACKED_STOCKS.items():
            dates = read_dates(path)
            futures.append(
                executor.submit(get_coin_data, ticker, dates)
            )

        results = [future.result() for future in futures]

        total_res = pd.concat(results)
        save_coin_data(DST_PATH, total_res)