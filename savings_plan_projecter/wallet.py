from dataclasses import dataclass


@dataclass
class Stock:
    """Represents a stock."""

    symbol: str
    investment: float
    countervalue: float | None = None

    def __post_init__(self) -> None:
        if self.investment <= 0:
            raise ValueError("Investment must be positive")
        if self.countervalue is None:
            self.countervalue = self.investment

    @property
    def return_on_investment(self) -> float:
        return self.countervalue / self.investment - 1

    def modify_position(self, by_amount: float) -> None:
        if self.countervalue + by_amount < 0:
            msg = f"Can't decrease position ({by_amount}) by more than its countervalue ({self.countervalue})"
            raise ValueError(msg)
        self.countervalue += by_amount
        self.investment += by_amount

    def apply_percentage_value_change(self, change: float) -> None:
        """Apply change expressed as a percentage where 0.1 is 10% increase."""
        self.countervalue *= 1 + change


class Wallet:
    def __init__(self, stocks: dict[str, Stock] | None = None) -> None:
        self.stocks = {} if stocks is None else stocks

    @property
    def investment(self) -> float:
        return sum(stock.investment for stock in self.stocks.values())

    @property
    def countervalue(self) -> float:
        return sum(stock.countervalue for stock in self.stocks.values())

    @property
    def return_on_investment(self) -> float:
        if self.is_empty():
            return 0
        return self.countervalue / self.investment - 1

    def is_empty(self) -> bool:
        return not self.stocks

    def buy(self, stock_name: str, amount: float) -> None:
        if stock_name in self.stocks:
            self.stocks[stock_name].modify_position(amount)
        else:
            self.stocks[stock_name] = Stock(stock_name, amount)

    def sell(self, stock_name: str, amount: float) -> None:
        if stock_name not in self.stocks:
            raise ValueError(f"Stock {stock_name} not in wallet")
        self.stocks[stock_name].modify_position(-amount)

    def apply_percentage_value_change(self, stock: str, change: float) -> None:
        """Apply change expressed as a percentage where 0.1 is 10% increase."""
        self.stocks[stock].apply_percentage_value_change(change)
