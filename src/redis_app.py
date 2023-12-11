# imports
import sys
import time
from mdp_collector import MDPCollector
from db import DB
from credentials import DB_USERNAME, DB_PASSWORD, DATABASE_NAME, RDS_HOSTNAME

TICKERS_FILE = "/opt/kalshi/tickers.txt"

if __name__ == "__main__":

    while True:

        collector = MDPCollector(tickers_file=TICKERS_FILE)
        db = DB(username=DB_USERNAME, password=DB_PASSWORD, host=RDS_HOSTNAME, database_name=DATABASE_NAME)
        last_orderbooks = {}

        while True:
            
            try:
                orderbooks = collector.update_orderbooks()
                for ticker, orderbook in orderbooks.items():
                    last_orderbook = last_orderbooks.get(ticker, {})
                    if last_orderbook != orderbook:
                        db.push_orderbook(ticker=ticker, orderbook=orderbook)
                    last_orderbooks[ticker] = orderbook
            except Exception as e:
                print(time.time(), e)
                break