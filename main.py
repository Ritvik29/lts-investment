from pprint import pprint
import finviz
from provider import get_stock_info_provider
import yfinance as yf

if __name__ == '__main__':
    # pprint(finviz.get_stock('MSFT'))
    # p = get_stock_info_provider("MSFT")
    # print(p.beta)
    # print(p.eps_next_5_years)
    # print(p.shares_outstanding)
    # msft = yf.Ticker("MSFT")
    # pprint(msft.get_cashflow(as_dict=True))

    # pprint(msft.info)

    p = get_stock_info_provider("MSFT")
    # print(p.cash_flow_growth_rate_1_5)
    output = p.operating_cash_flow_projected

    for i, o in enumerate(output):
        print(i + 2022, o)

    print(p.pv_of_20_year_cashflow)
    print(p.intrinsic_value_before_cash_debt)
    print(p.less_debt_per_share)
    print(p.plus_cash_per_share)
    print(p.final_intrinsic_value_per_share)
