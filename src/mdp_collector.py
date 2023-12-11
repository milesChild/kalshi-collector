# imports
from lib.kalshi_exchange_client import ExchangeClient

class MDPCollector():
    
    def __init__(self,
                 redis_address: str
                 ) -> None:
        """
        """
        # isolate all unique tickers based on existing keys in redis
        self.redis_address = redis_address
        self.tickers = self.get_tickers()
        self.orderbooks = {ticker: {} for ticker in self.tickers}
        self.update_orderbooks()
    
    def get_tickers(self) -> list:
        # queries for all unique keys in redis to find all tickers for this session
        return
    
    def update_orderbooks(self) -> None:
        # query redis for all current orderbook data
        pass