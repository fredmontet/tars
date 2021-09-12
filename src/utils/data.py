import pandas as pd
from pandas import DataFrame


def download_historical_data():
    """ Explanation about the download procedure of historical data """
    print("""To download historical data : \n 
        1. go on https://www.cryptodatadownload.com/data/binance/ \n
        2. download the Minutes files you want, \n
        3. put the file in the `data/raw/binance` folder.""")


def get_historical_ohlc_data(pair: str, start: str = None, end: str = None,
                             data_folder: str = '../data/raw/binance') \
        -> DataFrame:
    """ Get historical data in standard format

    Works only if data is available in CSV format from the data folder.

    :param pair: str
        The pair to get data for
    :param start: str (optional)
        Starting day, for instance: 2020-01-01
    :param end: str (optional)
        Ending day, for instance: 2020-31-12
    :param data_folder: str (optional)
        Folder where the raw data is stored

    :return: DataFrame
    """
    df = pd.read_csv(f"{data_folder}/Binance_{pair}_minute.csv", header=1)
    df = df.infer_objects()
    df['dtime'] = pd.to_datetime(df['date'])
    df = df.set_index('dtime')
    df = df.rename(columns={
        'unix': 'time',
        'tradecount': 'count',
        'Volume ETH': 'volume'
    })
    df = df.drop(columns=['symbol', 'date', 'Volume USDT'])

    if start is not None and end is not None:
        df = df[start:end]

    return df
