import pandas as pd
import numpy as np


__all__ = ['diff', 'ret', 'log_ret', 'smooth']


def diff(x, periods=1):

    """
    1st discrete difference

    :param x: time series
    :param periods: Periods to shift for forming difference
    :return:
    """

    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)
    return x.diff(periods)[periods:]


def ret(x, periods=1):

    """
    Percentage of change

    :param x:
    :param periods:
    :return:
    """
    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)
    return x.pct_change(periods)[periods:]


def log_ret(x, periods=1):

    """
    Log percentage of change

    :param x:
    :param periods:
    :return:
    """

    if not isinstance(x, pd.DataFrame):
        x = pd.DataFrame(x)
    return np.log(x).diff(periods).dropna()


def smooth(ts, method='mean', window=5):

    if method == 'mean':
        return ts.rolling(window=window).mean()

    if method == 'ewma':
        return ts.ewm(span=window).mean()

    raise Exception('Invalid method')
