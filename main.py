from pprint import pprint
import finviz
from provider import get_stock_info_provider
import yfinance as yf

from provider import get_stock_info_provider
from analyzer import get_intrinsic_value_calculator


if __name__ == '__main__':
    ticker = "MSFT"
    p = get_stock_info_provider(ticker)
    a = get_intrinsic_value_calculator(ticker, p)
    print(a.final_intrinsic_value_per_share)

