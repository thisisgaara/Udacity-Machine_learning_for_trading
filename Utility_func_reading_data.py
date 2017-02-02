"""Utility functions"""

import os
import pandas as pd

def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')
    dfSPY = pd.read_csv(symbol_to_path(symbols[0]), index_col = 'Date', parse_dates = True, usecols = ['Date', 'Adj Close'], na_values = ['nan'])
    dfSPY.rename(columns={'Adj Close':'SPY'}, inplace = True)
    df = df.join(dfSPY, how = 'inner');    
    for symbol in symbols:
        if symbol is not 'SPY':
            dfsymbol = pd.read_csv(symbol_to_path(symbol), index_col = 'Date', parse_dates = True, usecols = ['Date', 'Adj Close'], na_values = ['nan'])
            dfsymbol.rename(columns={'Adj Close':str(symbol)}, inplace = True)
            df = df.join(dfsymbol, how = 'inner')
    return df


def test_run():
    # Define a date range
    dates = pd.date_range('2010-01-22', '2010-01-26')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']
    
    # Get stock data
    df = get_data(symbols, dates)
    print df


if __name__ == "__main__":
    test_run()
