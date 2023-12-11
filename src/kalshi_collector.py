# imports
from lib.kalshi_exchange_client import ExchangeClient

KALSHIAPIBASE = "https://trading-api.kalshi.com/trade-api/v2"
REDISLOCATION = ""

class KalshiCollector():
    
    def __init__(self,
                 ticker: str,
                 username: str,
                 password: str
                 ) -> None:
        """
        """
        self.ticker = ticker
        self.exchange_client = self._init_kalshi_connection(username=username, password=password)

    def _init_kalshi_connection(self, 
                                username: str, 
                                password: str
                                ) -> ExchangeClient:
        
        exchange_client = ExchangeClient(exchange_api_base = KALSHIAPIBASE, email = username, password = password)

        return exchange_client
    
    def collect_orderbook(self) -> dict:
        """Get order book information for a given ticker."""

        orderbook = self.exchange_client.get_orderbook(ticker=self.ticker)['orderbook']
        # change the yes and no keys to bid and ask
        orderbook['bid'] = orderbook.pop('yes')
        orderbook['ask'] = orderbook.pop('no')

        return orderbook