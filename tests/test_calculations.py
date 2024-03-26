
import pytest
from app.calculations import add, BankAccount, InsufficientFundsExeption


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(1, 2, 3), (5, 7, 12), (23, 26, 49)])
def test_add(num1, num2, expected):
    assert expected == add(num1, num2)


def test_bank_account_initial_amount(bank_account):
    assert bank_account.balance == 50


def test_bank_account_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_account_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_bank_account_deposit(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70


def test_bank_account_collect_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 1) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (500, 200, 300),
    (450, 260, 190)
])
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert expected == zero_bank_account.balance

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFundsExeption):
      bank_account.withdraw(200)
