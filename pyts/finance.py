import pandas as pd
import pandas_datareader as pdr


__all__ = ['get_historical_data']


def get_historical_data(symbol, start, end, source='yahoo', ascending=True, usecols=None, fillna=None):

    """
    :param symbol: stock ticker.
    :param start: string date in format 'yyyy-mm-dd' ('2009-09-11').
    :param end: string date in format 'yyyy-mm-dd' ('2010-09-11').
    :param source:
    :param ascending: sort returning values in ascending or descending order based on Date column.
    :param usecols: List of columns to return. If None, return all columns.
    :param fillna:
    :return: DataFrame
    """

    dt = pdr.DataReader(symbol, data_source=source, start=start, end=end, retry_count=20)

    if usecols is not None:
        dt = dt.filter(items=usecols)

    dt = dt.sort_index(axis=1 if isinstance(symbol, list) else 0, ascending=ascending)

    if fillna is not None:
        all_weekdays = pd.date_range(start=start, end=end, freq='B')
        dt = dt.reindex_axis(all_weekdays, 1 if isinstance(symbol, list) else 0, method=fillna)

    if isinstance(symbol, list):
        return {s: dt.minor_xs(s) for s in symbol}
    else:
        return dt
