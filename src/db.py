# imports
import pymysql
import json
from datetime import datetime

class DB():

    def __init__(self, username: str, password: str, host: str, database_name: str) -> None:
        
        self.connection = pymysql.connect(host=host, user=username, password=password, database=database_name, autocommit=True)
        self.cursor = self.connection.cursor()
        self.cursor.execute('select version()')
    
    def push_orderbook(self, ticker: str, orderbook: dict) -> None:
        
        orderbook_json = json.dumps(orderbook)
        time = datetime.now()
        self.cursor.execute("""INSERT INTO orderbooks (time, ticker, orderbook) VALUES (%s, %s, %s)""", (time, ticker, orderbook_json))