from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager, AbstractContextManager
import requests
import datetime
from money import Money


class BaseBank(ABC):
    def __init__(self, login_url, accounts_url, movements_url, logout_url):
        self.login_url = login_url
        self.accounts_url = accounts_url
        self.movements_url = movements_url
        self.logout_url = logout_url


class InvalidCredentialsException(Exception):
    pass


class BankLogin(ABC):
    pass


class UserPasswordBankLogin(BankLogin):
    def __init__(self, username, password):
        self.username = username
        self.password = password


class Bank(BaseBank):
    def __init__(self, name, baseBank, credentials, session=requests.Session()):

        super().__init__(
            baseBank.login_url,
            baseBank.accounts_url,
            baseBank.movements_url,
            baseBank.logout_url,
        )
        self.name = name
        self.credentials = credentials
        self._session = session
        self.is_logged_in = False

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.logout()

    @abstractmethod
    def login(self):
        pass

    @abstractmethod
    def fetch_accounts(self):
        pass

    @abstractmethod
    def get_account(self, number):
        pass

    @abstractmethod
    def logout(self):
        pass

    def _fetch(self, url, data=None, headers=None):
        if data is None:
            return self._session.get(url).content
        else:
            r = self._session.post(url, data=data, headers=headers)
            return r.text


class AbstractBankAccount(ABC):
    def __init__(
        self, bank, account_number, alias, type, currency, account_bank_reference=None
    ):
        self.bank = bank
        self.account_number = account_number
        self.alias = alias
        self.type = type
        self.currency = currency
        self.account_bank_reference = account_bank_reference

    def __str__(self):
        return "{0} - {1} - {2} - {3} - {4} - {5}".format(
            self.bank.name,
            self.account_number,
            self.alias,
            self.type,
            self.currency,
            self.account_bank_reference,
        )

    @abstractmethod
    def fetch_movements(self, start_date, end_date):
        pass


class Movement:
    def __init__(
        self,
        account,
        transaction_id,
        date,
        description,
        ammount,
        alternative_transaction_id=None,
    ):
        self.account = account
        self.transaction_id = transaction_id
        self.alternative_transaction_id = alternative_transaction_id
        self.date = date
        self.description = description
        self.ammount = ammount
        self.is_debit = ammount < Money(0, currency="GTQ")
        self.is_credit = ammount > Money(0, currency="GTQ")
        self.is_fund_regulation = ammount == Money(0, currency="GTQ")

    def __str__(self):
        return "{0} - {1} - {2} - {3} - {4}".format(
            self.account.account_number,
            self.transaction_id,
            self.date,
            self.description,
            self.ammount,
        )
