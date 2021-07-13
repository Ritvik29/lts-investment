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
    msft = yf.Ticker("MSFT")
    # pprint(msft.get_cashflow(as_dict=True))
    # pprint(msft.info)
    # Short Long Term Debt
    # Long Term Debt
    # pprint(msft.quarterly_balancesheet)
    # 2021-03-31
    # total = msft.quarterly_balancesheet.loc['Short Long Term Debt'] + msft.quarterly_balancesheet.loc['Long Term Debt']
    # print(total)
    # print(total[0])
    # print(msft.quarterly_balancesheet.loc['Short Long Term Debt'][0])
    # pprint(msft.quarterly_balancesheet.loc['Intangible Assets'])
    # Short Long Term Debt              8.051000e+09  ...  3.749000e+09
    # Long Term Debt                    5.000700e+10  ...  5.957800e+10
    # pprint(msft.info)

    sb = msft.quarterly_balancesheet
    # print(sb)
    cash = sb.loc['Cash'][0]
    sti = sb.loc['Short Term Investments'][0]
    print('*' * 20)
    print(cash)
    print(sti)
    print((cash + sti) / 10**6)

    #######
    p = get_stock_info_provider("MSFT")
    # # print(p.cash_flow_growth_rate_1_5)
    # output = p.operating_cash_flow_projected
    #
    # for i, o in enumerate(output):
    #     print(i + 2022, o)

    # print(p.pv_of_20_year_cashflow)
    # print(p.intrinsic_value_before_cash_debt)
    # print(p.less_debt_per_share)
    # print(p.plus_cash_per_share)
    # print(p.final_intrinsic_value_per_share)
    # print(p.total_debt)
    print(p.final_intrinsic_value_per_share)
    print(p.final_intrinsic_value_per_share )