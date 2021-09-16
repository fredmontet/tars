import pandas as pd
from pandas import DataFrame


def download_historical_data():
    """ Explanation about the download procedure of historical data """
    print("""To download historical data (updated every quarter) : \n
        1. go on https://drive.google.com/drive/folders/1sqt3kvw_Y5yOfF6HLG_xfAXae0LsVZWH\n
        2. download one of the separate zip file \n
        3. put the file in the `data/raw/` folder.""")


def get_historical_ohlc_data(base: str, quote: str, interval: int = 5, start: str = None, end: str = None,
                             data_folder: str = '../data/raw/') \
        -> DataFrame:
    """ Get historical data in standard format

    Works only if data is available in CSV format from the data folder.

    :param base: str
        The base currency e.g. ETH
    :param quote: str
        The quote currency e.g. USD
    :param interval: int
        The candle interval. Must be 1, 5, 15, 60, 720 or 1440
    :param start: str (optional)
        Starting day, for instance: 2020-01-01
    :param end: str (optional)
        Ending day, for instance: 2020-31-12
    :param data_folder: str (optional)
        Folder where the raw data is stored

    :return: DataFrame
    """

    available_intervals = [1, 5, 15, 60, 720, 1440]
    assert interval in available_intervals, f'The interval {interval} is not supported, please choose one of {available_intervals}'

    cols = ['open','high','low','close','volume','trades']
    df = pd.read_csv(f"{data_folder}/{base}_OHLCVT/{base+quote}_{interval}.csv", names=cols)
    df = df.infer_objects()
    df['timestamp'] = pd.to_datetime(df.index, unit='s')
    df = df.set_index('timestamp')

    if start is not None and end is not None:
        df = df[start:end]

    return df
