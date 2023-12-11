# imports
from lib.kalshi_exchange_client import ExchangeClient
import redis

class MDPCollector():
    
    def __init__(self,
                 tickers_file: str,
                 ) -> None:
        """
        """
        # isolate all unique tickers based on existing keys in redis
        self.redis_client = redis.Redis()
        self.tickers = self.get_tickers(file_location=tickers_file)
        self.orderbooks = {ticker: {} for ticker in self.tickers}
        self.update_orderbooks()
    
    def get_tickers(self, file_location) -> list:
        # reads from the tickers file to init all the tickers for which we will listen for orderbooks in redis
        with open(file_location, "r") as f:
            tickers = f.read().splitlines()
        return tickers
    
    def update_orderbooks(self) -> None:
        # query redis for all current orderbook data
        for ticker in self.tickers:
            ob = self.redis_client.hgetall(ticker)
            self.orderbooks[ticker] = ob