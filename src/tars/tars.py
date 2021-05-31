import requests


def get_pair(pair):
    r = requests.get(f'https://api.kraken.com/0/public/Ticker?pair={pair}')
    return r.json()
    