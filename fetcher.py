import requests
import csv

# API Docs
# https://www.alphavantage.co/documentation/#intraday
# https://www.alphavantage.co/documentation/#intraday-extended

class ApiFetcher:
    def __init__(self, url, apikey) -> None:
        self.url = url
        self.apikey = apikey
        
    # Save data from last 1-2 months: depends on size parameter
    def save_intraday_history(self, symbol, interval, size, file_name):
        with requests.Session() as s:
            download = s.get(
                self.url,
                params = {
                    'function': 'TIME_SERIES_INTRADAY',
                    'symbol': symbol, 
                    'interval': interval, 
                    'output_size': size, 
                    'datatype' : "csv",
                    'apikey': self.apikey
                },
            )
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)
            with open(file_name, 'a', newline ='') as file:
                write = csv.writer(file)
                write.writerows(rows) 

    # Save data belonging to the last two years (A lot of data)
    def save_extended_history_full(self, symbol, interval, file_name):
        for i in range(24):
            slice = f'year{(i // 12) + 1}month{(i % 12) + 1}'
            self.save_extended_history_slice(symbol, interval, slice, file_name)

    # Save data from last 1 month belonging to the last two years: depends on slice parameter
    def save_extended_history_slice(self, symbol, interval, slice, file_name):
        with requests.Session() as s:
            download = s.get(
                self.url,
                params = {
                    'function': 'TIME_SERIES_INTRADAY_EXTENDED',
                    'symbol': symbol, 
                    'interval': interval, 
                    'slice': slice, 
                    'apikey': self.apikey
                },
            )
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            rows = list(cr)
            with open(file_name, 'a', newline ='') as file:
                write = csv.writer(file)
                write.writerows(rows) 

key = "F7EGKU798BQ8Z02H"
url = "https://www.alphavantage.co/query"
fetcher = ApiFetcher(url, key)

# fetcher.save_intraday_history("IBM", "5min", "compact", "stocks.csv")
# fetcher.save_extended_history_full("IBM", "5min", "stocks_full.csv")