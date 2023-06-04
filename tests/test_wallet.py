import pytest

from savings_plan_projecter.wallet import Stock, Wallet


@pytest.mark.parametrize("investment", (0, -100))
def test_if_investment_is_non_positive_then_error(investment):
    with pytest.raises(ValueError):
        Stock("S&P500", investment=investment)


def test_if_no_countervalue_provided_then_countervalue_is_investment():
    mystock = Stock("S&P500", investment=100)
    assert mystock.countervalue == 100
    assert mystock.investment == 100


def test_if_change_position_then_countervalue_and_investment_change():
    mystock = Stock("S&P500", investment=100)
    mystock.modify_position(100)
    assert mystock.countervalue == 200
    assert mystock.investment == 200
    mystock.modify_position(-50)
    assert mystock.countervalue == 150
    assert mystock.investment == 150


def test_if_change_position_leads_to_negative_countervalue_then_error():
    mystock = Stock("S&P500", investment=100)
    with pytest.raises(ValueError):
        mystock.modify_position(-200)


def test_value_change_modifies_countervalue():
    mystock = Stock("S&P500", investment=100)
    mystock.apply_percentage_value_change(0.10)
    assert mystock.countervalue == pytest.approx(110)
    assert mystock.investment == 100


def test_stock_return_is_ration_of_countervalue_to_investment():
    mystock = Stock("S&P500", investment=100)
    assert mystock.return_on_investment == 0
    mystock.apply_percentage_value_change(0.10)
    assert mystock.return_on_investment == pytest.approx(0.1)


def test_if_new_stock_is_bought_then_it_is_added_to_stocks():
    wallet = Wallet()
    wallet.buy("S&P500", 100)
    assert wallet.stocks == {"S&P500": Stock("S&P500", 100)}


def test_if_stock_already_in_wallet_then_add_amount():
    wallet = Wallet({"S&P500": Stock("S&P500", 100)})
    wallet.buy("S&P500", 100)
    assert wallet.stocks == {"S&P500": Stock("S&P500", 200)}


def test_if_sell_stock_not_in_wallet_then_error():
    wallet = Wallet()
    with pytest.raises(ValueError):
        wallet.sell("S&P500", 100)


def test_if_sell_stock_in_wallet_then_subtract_amount():
    wallet = Wallet({"S&P500": Stock("S&P500", 100)})
    wallet.sell("S&P500", 50)
    assert wallet.stocks == {"S&P500": Stock("S&P500", 50)}


def test_if_sell_more_of_a_stock_than_in_wallet_then_error():
    wallet = Wallet({"S&P500": Stock("S&P500", 100)})
    with pytest.raises(ValueError):
        wallet.sell("S&P500", 200)


def test_if_wallet_has_no_stocks_then_is_empty():
    wallet = Wallet()
    assert wallet.is_empty()


def test_if_wallet_is_empty_then_return_on_investment_is_zero():
    wallet = Wallet()
    assert wallet.return_on_investment == 0


def test_if_wallet_not_empty_then_return_on_investments_is_ratio_countervalue_to_investment():
    wallet = Wallet(
        {"S&P500": Stock("S&P500", 100, 110), "AAPL": Stock("AAPL", 100, 130)}
    )
    assert wallet.return_on_investment == pytest.approx(0.2)
