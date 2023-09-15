# imports
import sys
import time
from src.kalshi_collector import KalshiCollector
from src.db import DB
from credentials import DB_PASSWORD, DB_USERNAME

if __name__ == "__main__":

    # Get ticker from command line
    ticker = str(sys.argv[1])

    while True:

        collector = KalshiCollector(ticker=ticker)
        db = DB(username=DB_USERNAME, password=DB_PASSWORD)

        while True:

            try:
                orderbook = collector.collect_orderbook()
                db.push_orderbook(ticker=ticker, orderbook=orderbook)
            except Exception as e:
                print(time.time(), e)
                break