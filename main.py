from pprint import pprint
import finviz
from provider import get_stock_info_provider
import yfinance as yf

from provider import get_stock_info_provider
from analyzer import get_intrinsic_value_calculator

if __name__ == '__main__':
    # ticker = "JNJ"
    # # ticker = "MSFT"
    # p = get_stock_info_provider(ticker)
    # a = get_intrinsic_value_calculator(ticker, p)
    # # print(a.pv_of_20_year_cashflow)
    # # print(a.intrinsic_value_before_cash_debt)
    # # print(a.less_debt_per_share)
    # # print(a.plus_cash_per_share)
    # # print(a.operating_cash_flow_projected)
    # print(a.final_intrinsic_value_per_share)
    # print(a.discount)

    tickers = [
        "MA",
        "JPM",
        "BAC",
        "AAPL",
        "MSFT",
        "CRM",
        "NOW",
        "PG",
        "PEP",
        "MMM",
        "BA",
        "JNJ",
        "UNH",
        "FB",
        "GOOGL",
        "AMZN",
        "HD",
        "NKE"
    ]

    # for ticker in tickers:
    #     p = get_stock_info_provider(ticker)
    #     a = get_intrinsic_value_calculator(ticker, p)
    #
    #     try:
    #         print("{}: {}".format(ticker, a.final_intrinsic_value_per_share))
    #     except Exception as e:
    #         print("{}: {}".format(ticker, e))

    ticker = 'MSFT'
    p = get_stock_info_provider(ticker)
    a = get_intrinsic_value_calculator(ticker, p)
    print(a.operating_cash_flow_projected)
    print(a.intrinsic_value_before_cash_debt)
    print(a.less_debt_per_share)
    print(a.plus_cash_per_share)
    print(a.final_intrinsic_value_per_share)

    print(p.operating_cashflow)


