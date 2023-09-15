# imports
import sys
import time
from kalshi_collector import KalshiCollector
from db import DB
from src.credentials import DB_USERNAME, DB_PASSWORD, DATABASE_NAME, RDS_HOSTNAME, KALSHI_EMAIL, KALSHI_PASSWORD

if __name__ == "__main__":

    # Get ticker from command line
    ticker = str(sys.argv[1])

    while True:

        kc = KalshiCollector(ticker=ticker, username=KALSHI_EMAIL, password=KALSHI_PASSWORD)
        db = DB(username=DB_USERNAME, password=DB_PASSWORD, host=RDS_HOSTNAME, database_name=DATABASE_NAME)

        while True:

            try:
                orderbook = kc.collect_orderbook()
                print(time.time(), ticker, orderbook)
                db.push_orderbook(ticker=ticker, orderbook=orderbook)
            except Exception as e:
                print(time.time(), e)
                break