# # imports
# from src.lib.kalshi_exchange_client import ExchangeClient
# from datetime import datetime, timezone as tz, timedelta
# from src.credentials import KALSHI_EMAIL, KALSHI_PASSWORD

# KALSHIAPIBASE = "https://demo-api.kalshi.co/trade-api/v2"

# DAILY_SERIES = [
#     "NASDAQ100",  # <-- Nasdaq 100 daily close
#     "INX"  # <-- S&P 500 daily close
# ]

# WEEKLY_SERIES = [
#     "INXW",
#     "NASDAQ100W"
# ]

# TICKERS_FILE_PATH = "/opt/kalshi/tickers.txt"

# def date_selector(polygon: bool=False) -> str:
#     """
#     Uses the current time to select the month, date string to represent
#     the date of the contract we want to trade.

#     If it is past 4:00pm EST, we will select the next trading day's date.

#     If it is before 4:00pm EST, we will select the current day's date.

#     The returning string will be formatted like: AUG14
#     """
#     # Get the current time in EST
#     now = datetime.now(tz=tz.utc) - timedelta(hours=4)
#     # If it is a weekend, select the closest weekday
#     if now.weekday() > 4:
#         next_trading_day = now + timedelta(days=3 - (now.weekday() - 4))
#         date_str = next_trading_day.strftime("%b%d").upper()
#     # If it is past 3:55pm EST, we will select the next trading day's date.
#     elif now.hour >= 16 or (now.hour == 15 and now.minute >= 55):
#         # if it is on or past friday, add the correct number of days to get to monday
#         if now.weekday() >= 4:
#             next_trading_day = now + timedelta(days=3 - (now.weekday() - 4))
#         else:
#             next_trading_day = now + timedelta(days=1)

#         date_str = next_trading_day.strftime("%b%d").upper()
#     else:
#         # If it is before 4:00pm EST, we will select the current day's date.
#         date_str = now.strftime("%b%d").upper()

#     if polygon:
#         # Convert date_str to "%Y-%m-%d" format
#         date = datetime.strptime(f"{date_str} {now.year}", "%b%d %Y")
#         date_str = date.strftime("%Y-%m-%d")
#         return date_str
#     else:
#         return date_str

# exchange_client = ExchangeClient(exchange_api_base = KALSHIAPIBASE, email = KALSHI_EMAIL, password = KALSHI_PASSWORD)

# agg_tickers = []
# today_str = date_selector()
# today = datetime.strptime(today_str, "%b%d").date()
# day_of_week = today.weekday()
# if day_of_week == 5:
#     weekly = True
# else:
#     weekly = False

# """ Bracket Tickers """

# # SPX
# spx_tickers = []

# spx_series = "INXW" if weekly else "INX"

# markets = exchange_client.get_markets(**{'series_ticker': spx_series})['markets']
# filtered = [x for x in markets if today_str in x['ticker']]
# tickers = [x['ticker'] for x in filtered]
# for t in tickers:
#     if t not in spx_tickers:
#         spx_tickers.append(t)
# agg_tickers.extend(spx_tickers)

# # NDX
# ndx_tickers = []

# ndx_series = "NASDAQ100W" if weekly else "NASDAQ100"

# markets = exchange_client.get_markets(**{'series_ticker': ndx_series})['markets']
# filtered = [x for x in markets if today_str in x['ticker']]
# tickers = [x['ticker'] for x in filtered]
# for t in tickers:
#     if t not in ndx_tickers:
#         ndx_tickers.append(t)
# agg_tickers.extend(ndx_tickers)

import json
import requests
from src.lib.kalshi_exchange_client import ExchangeClient
from src.credentials import KALSHI_EMAIL, KALSHI_PASSWORD
KALSHIAPIBASE = "https://trading-api.kalshi.com/trade-api/v2"
TICKERS_FILE_PATH = "/opt/kalshi/tickers.txt"

PREFIXES = [
    "INXD", # range
    "INXDU", # above/below
    "INXZ", # up/down
    "NASDAQ100DU", # above/below
    "NASDAQ100D", # range
    "NASDAQ100Z", # up/down
]

exchange_client = ExchangeClient(exchange_api_base = KALSHIAPIBASE, email = KALSHI_EMAIL, password = KALSHI_PASSWORD)

headers = {"accept": "application/json"}
params = {"status": "open"}
url="https://trading-api.kalshi.com/trade-api/v2/events"
response = requests.get(url, headers=headers, params=params)
data = json.loads(response.text)

event_tickers = [x['event_ticker'] for x in data['events']]
filtered_event_tickers = [x for x in event_tickers if x.split('-')[0] in PREFIXES]

# get all tickers for each event ticker in filtered_event_tickers
all_tickers = []
for event_ticker in filtered_event_tickers:
    data = exchange_client.get_markets(event_ticker=event_ticker)
    tickers = [x['ticker'] for x in data['markets']]
    all_tickers.extend(tickers)

all_tickers

# """ Writing to File """

# Write tickers to the specified TICKERS_FILE_PATH as a text file with each ticker on a new line
with open(TICKERS_FILE_PATH, 'w') as f:
    for ticker in all_tickers:
        f.write(ticker + '\n')
