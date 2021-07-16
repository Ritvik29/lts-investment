from __future__ import absolute_import

import functools

import finviz
import yfinance

from .utils import to_million, billion_to_million


class StockInfoProvider:
    def __init__(self, ticker: str):
        self._ticker = ticker

    @property
    def beta(self) -> float:
        raise NotImplementedError

    @property
    def total_shares(self) -> int:
        raise NotImplementedError

    @property
    def eps_next_5_years(self) -> float:
        raise NotImplementedError

    @property
    def previous_close(self) -> float:
        raise NotImplementedError

    @property
    def operating_cashflow(self) -> float:
        raise NotImplementedError

    @property
    def total_cash(self) -> float:
        raise NotImplementedError

    @property
    def total_debt(self) -> float:
        raise NotImplementedError

    @property
    def last_close(self) -> float:
        raise NotImplementedError

    @property
    def ops_cashflow(self) -> float:
        raise NotImplementedError

    @property
    def shares_outstanding(self) -> int:
        raise NotImplementedError

    @property
    def ticker(self) -> str:
        return self._ticker


class FinvizProvider(StockInfoProvider):
    @functools.cached_property
    def _finviz_info(self):
        return finviz.get_stock(self._ticker)

    @property
    def beta(self) -> float:
        return float(self._finviz_info.get('Beta'))

    @property
    def total_shares(self) -> int:
        return billion_to_million(self._finviz_info.get('Shs Outstand'))

    @property
    def eps_next_5_years(self) -> float:
        return float(self._finviz_info.get('EPS next 5Y')[:-1])

    @property
    def previous_close(self) -> float:
        raise NotImplementedError

    @property
    def operating_cashflow(self) -> float:
        raise NotImplementedError

    @property
    def total_cash(self) -> float:
        raise NotImplementedError

    @property
    def total_debt(self) -> float:
        raise NotImplementedError


class YahooProvider(StockInfoProvider):
    @functools.cached_property
    def _yahoo_finance(self):
        return yfinance.Ticker(self.ticker)

    @property
    def beta(self) -> float:
        raise NotImplementedError

    @property
    def total_shares(self) -> int:
        raise NotImplementedError

    @property
    def eps_next_5_years(self) -> float:
        raise NotImplementedError

    @property
    def previous_close(self) -> float:
        return self._yahoo_finance.info.get('previousClose')

    @property
    def operating_cashflow(self) -> float:
        return to_million(self._yahoo_finance.info.get('operatingCashflow'))

    @property
    def total_cash(self) -> float:
        return to_million(self._yahoo_finance.info.get('totalCash'))

    @property
    def total_debt(self) -> float:
        balancesheet = self._yahoo_finance.quarterly_balancesheet
        debt = balancesheet.loc['Short Long Term Debt'][0] + balancesheet.loc['Long Term Debt'][0]
        return to_million(debt)


class HybridProvider(StockInfoProvider):
    def __init__(self, ticker: str, finviz_provider: FinvizProvider, yahoo_provider: YahooProvider):
        super().__init__(ticker)
        self._yahoo = yahoo_provider
        self._finviz = finviz_provider

    @property
    def beta(self) -> float:
        return self._finviz.beta

    @property
    def previous_close(self) -> float:
        return self._yahoo.previous_close

    @property
    def operating_cashflow(self) -> float:
        return self._yahoo.operating_cashflow

    @property
    def total_cash(self) -> float:
        return self._yahoo.total_cash

    @property
    def total_debt(self) -> float:
        return self._yahoo.total_debt

    @property
    def total_shares(self) -> int:
        return self._finviz.total_shares

    @property
    def eps_next_5_years(self) -> float:
        return self._finviz.eps_next_5_years


def get_stock_info_provider(ticker: str) -> StockInfoProvider:
    return HybridProvider(
        ticker,
        finviz_provider=FinvizProvider(ticker),
        yahoo_provider=YahooProvider(ticker),
    )
