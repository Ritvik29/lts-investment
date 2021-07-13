from __future__ import absolute_import

import finviz
import yfinance

import functools
from .utils import billion_to_million, to_million


class StockInfoProvider:
    @property
    def ticker(self):
        raise NotImplementedError

    @property
    def eps_next_5_years(self):
        raise NotImplementedError

    @property
    def cash_flow_growth_rate_1_5(self):
        return self.eps_next_5_years

    @property
    def cash_flow_growth_rate_6_10(self):
        return self.cash_flow_growth_rate_1_5 / 2.0

    @property
    def cash_flow_growth_rate_11_20(self):
        return 4.18

    def flow_rate(self, after_years):
        if after_years <= 5:
            return self.cash_flow_growth_rate_1_5
        if after_years <= 10:
            return self.cash_flow_growth_rate_6_10
        if after_years <= 20:
            return self.cash_flow_growth_rate_11_20

        raise ValueError("Years should beb between 1-20 inclusive")

    @property
    def operating_cash_flow_projected(self):
        output = [
            (self.operating_cash_flow_current, 1, self.operating_cash_flow_current)
        ]

        for i in range(20):
            x = output[i][0] * (1 + self.flow_rate(after_years=i + 1) / 100)
            y = output[i][1] / (1 + self.discount_rate)
            z = x * y
            output.append((x, y, z))

        return output[1:]

    @property
    def discount_rate(self) -> float:
        rates = [
            (0.80, 5),
            (1, 5.9),
            (1.1, 6.3),
            (1.2, 6.7),
            (1.3, 7.2),
            (1.4, 7.6),
            (1.5, 8.0),
            (float('inf'), 8.4)
        ]

        for limit, rate in rates:
            if self.beta < limit:
                return rate / 100

    @property
    def pv_of_20_year_cashflow(self):
        return sum([
            v for (_, _, v) in self.operating_cash_flow_projected
        ])

    @property
    def intrinsic_value_before_cash_debt(self):
        shares = self.shares_outstanding
        return self.pv_of_20_year_cashflow / shares if shares else 0

    @property
    def less_debt_per_share(self):
        shares = self.shares_outstanding
        return self.total_debt / shares if shares else 0

    @property
    def plus_cash_per_share(self):
        shares = self.shares_outstanding
        return self.total_cash / shares if shares else 0

    @property
    def final_intrinsic_value_per_share(self):
        return self.intrinsic_value_before_cash_debt + self.plus_cash_per_share - self.less_debt_per_share

    @property
    def shares_outstanding(self):
        raise NotImplementedError

    @property
    def beta(self):
        raise NotImplementedError

    @property
    def ops_cash_flow(self):
        raise NotImplementedError

    @property
    def operating_cash_flow_current(self):
        return self.ops_cash_flow

    @property
    def ttm_cash_flow(self):
        return self.ops_cash_flow

    @property
    def total_cash(self):
        raise NotImplementedError

    @property
    def total_debt(self):
        raise NotImplementedError

    @property
    def previous_close(self):
        raise NotImplementedError

    @property
    def last_close(self):
        return self.previous_close


class StockInfoProviderImplementation(StockInfoProvider):
    @property
    def ticker(self):
        return self._ticker

    @functools.cached_property
    def _yahoo_finance(self):
        return yfinance.Ticker(self.ticker)

    @property
    def previous_close(self):
        return self._yahoo_finance.info.get('previousClose')

    def __init__(self, ticker: str):
        self._ticker = ticker

    @functools.cached_property
    def _finviz_info(self):
        return finviz.get_stock(self._ticker)

    @property
    def eps_next_5_years(self) -> float:
        # Remove percentage % at the end of the str
        return float(self._finviz_info.get('EPS next 5Y')[:-1])

    @property
    def shares_outstanding(self) -> float:
        return billion_to_million(self._finviz_info.get('Shs Outstand'))

    @property
    def beta(self) -> float:
        return float(self._finviz_info.get('Beta'))

    @property
    def ops_cash_flow(self):
        return to_million(self._yahoo_finance.info.get('operatingCashflow'))

    @property
    def total_cash(self):
        return to_million(self._yahoo_finance.info.get('totalCash'))

    @property
    def total_debt(self):
        balancesheet = self._yahoo_finance.quarterly_balancesheet
        debt = balancesheet.loc['Short Long Term Debt'][0] + balancesheet.loc['Long Term Debt'][0]
        return to_million(debt)


def get_stock_info_provider(ticker: str):
    return StockInfoProviderImplementation(ticker)
