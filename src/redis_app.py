# imports
import sys
import time
from mdp_collector import MDPCollector
from db import DB
from credentials import DB_USERNAME, DB_PASSWORD, DATABASE_NAME, RDS_HOSTNAME, KALSHI_EMAIL, KALSHI_PASSWORD

REDIS_LOCATION = ""

if __name__ == "__main__":

    while True:

        collector = MDPCollector(redis_address=REDIS_LOCATION)
        db = DB(username=DB_USERNAME, password=DB_PASSWORD, host=RDS_HOSTNAME, database_name=DATABASE_NAME)
        last_orderbooks = {}

        while True:
            
            try:
                orderbooks = collector.update_orderbooks()
                if last_orderbooks != orderbooks:
                    db.push_orderbook(ticker=ticker, orderbook=orderbook)
                    print(time.time(), ticker, orderbook)
                last_orderbook = orderbook
            except Exception as e:
                print(time.time(), e)
                break