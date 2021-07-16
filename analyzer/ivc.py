from provider import StockInfoProvider, get_stock_info_provider

US = 'us'
CHINA = 'ch'
HONG_KONG = 'hk'


def discount_rate(beta: float) -> float:
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
        if beta <= limit:
            return rate / 100


def cashflow_growth_rate_20_years(country: str) -> float:
    if country == US:
        return 1.48
    return 7.0


class IntrinsicValueCalculator:
    @property
    def pv_of_20_year_cashflow(self) -> float:
        raise NotImplementedError

    @property
    def intrinsic_value_before_cash_debt(self) -> float:
        raise NotImplementedError

    @property
    def less_debt_per_share(self) -> float:
        raise NotImplementedError

    @property
    def plus_cash_per_share(self) -> float:
        raise NotImplementedError

    @property
    def final_intrinsic_value_per_share(self) -> float:
        raise NotImplementedError

    @property
    def discount(self) -> float:
        raise NotImplementedError

    @property
    def operating_cash_flow_projected(self) -> list[tuple[float, float, float]]:
        raise NotImplementedError


class IntrinsicValueCalculatorImplementation(IntrinsicValueCalculator):
    def __init__(self, ticker: str, stock_info_provider: StockInfoProvider, country: str):
        self._ticker = ticker
        self._country = country
        self._provider = stock_info_provider

    @property
    def pv_of_20_year_cashflow(self) -> float:
        return sum([
            v for (_, _, v) in self.operating_cash_flow_projected
        ])

    def flow_rate(self, after_years) -> float:
        eps_next_5y = self._provider.eps_next_5_years

        if after_years <= 5:
            return eps_next_5y
        if after_years <= 10:
            return eps_next_5y / 2
        if after_years <= 20:
            return cashflow_growth_rate_20_years(self._country)

        raise ValueError("Years should beb between 1-20 inclusive")

    @property
    def operating_cash_flow_projected(self) -> list[tuple[float, float, float]]:
        output = [
            (self._provider.operating_cashflow, 1, self._provider.operating_cashflow)
        ]

        for i in range(20):
            x = output[i][0] * (1 + self.flow_rate(after_years=i + 1) / 100)
            y = output[i][1] / (1 + discount_rate(self._provider.beta))
            z = x * y
            output.append((x, y, z))

        return output[1:]

    @property
    def intrinsic_value_before_cash_debt(self) -> float:
        shares = self._provider.shares_outstanding
        return self.pv_of_20_year_cashflow / shares if shares else 0.0

    @property
    def less_debt_per_share(self) -> float:
        shares = self._provider.shares_outstanding
        return self._provider.total_debt / shares if shares else 0.0

    @property
    def plus_cash_per_share(self) -> float:
        shares = self._provider.shares_outstanding
        return self._provider.total_cash / shares if shares else 0.0

    @property
    def final_intrinsic_value_per_share(self) -> float:
        return self.intrinsic_value_before_cash_debt \
               + self.plus_cash_per_share \
               - self.less_debt_per_share

    @property
    def discount(self) -> float:
        return 100 * ((self._provider.last_close / self.final_intrinsic_value_per_share) - 1)


def get_intrinsic_value_calculator(ticker: str,
                                   stock_info_provider: StockInfoProvider = None,
                                   stock_country: str = US) -> IntrinsicValueCalculator:
    if not stock_info_provider:
        stock_info_provider = get_stock_info_provider(ticker)
    return IntrinsicValueCalculatorImplementation(ticker, stock_info_provider, stock_country)
