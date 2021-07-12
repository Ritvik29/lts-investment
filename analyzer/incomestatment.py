import provider.stockinfo


class IncomeStatementAnalyzer:
    def __init__(self, stock_info_provider: provider.StockInfoProvider = None):
        self.provider = stock_info_provider

    @property
    def revenue(self):
        raise NotImplementedError

    @property
    def gross_profit(self):
        raise NotImplementedError

    @property
    def operating_income(self):
        raise NotImplementedError

    @property
    def ebit(self):
        return self.operating_income

    @property
    def earnings(self):
        raise NotImplementedError

    @property
    def profit(self):
        return self.earnings

    @property
    def gpm(self):
        raise NotImplementedError

    @property
    def npm(self):
        raise NotImplementedError

    def __dict__(self):
        return dict(
            revenue=self.revenue,
            gross_profit=self.gross_profit,
            operating_incom=self.operating_income,
            ebit=self.ebit,
            earnings=self.earnings,
            profit=self.profit,
            gpm=self.gpm,
            npm=self.npm
        )