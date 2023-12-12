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
        
        converted_dict = {key.decode('utf-8'): value.decode('utf-8') for key, value in orderbook.items()}
        orderbook_json = json.dumps(converted_dict)
        time = datetime.now()
        self.cursor.execute("""INSERT INTO orderbooks (time, ticker, orderbook) VALUES (%s, %s, %s)""", (time, ticker, orderbook_json))