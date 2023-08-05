# -*- coding: UTF-8 -*-

from os.path import dirname, join, realpath
from sys import modules

ROOT: str = dirname(realpath(modules["__main__"].__file__))
ENVIRONMENT: str = "production"  # or: "sandbox"
CACHE: str = join(ROOT, "cache", "exchange_cache")

EXCHANGE: dict = {
    "production": r"api.exchange.coinbase.com",
    "sandbox": r"api-public.sandbox.exchange.coinbase.com",
}

MARKET_DATA: dict = {
    "production": "ws-feed.exchange.coinbase.com",
    "sandbox": "ws-feed-public.sandbox.exchange.coinbase.com",
}

DIRECT_MARKET_DATA: dict = {
    "production": "ws-direct.exchange.coinbase.com",
    "sandbox": "ws-direct.sandbox.exchange.coinbase.com",
}

ENDPOINTS: dict = {
    "Time": "time",
    "Accounts": "accounts",
    "AddressBook": "address-book",
    "CoinbaseAccounts": "coinbase-accounts",
    "Conversions": "conversions",
    "Currencies": "currencies",
    "Deposits": "deposits",
    "PaymentMethods": "payment-methods",
    "Transfers": "transfers",
    "Withdrawals": "withdrawals",
    "Fees": "fees",
    "Fills": "fills",
    "Orders": "orders",
    "Oracle": "oracle",
    "Products": "products",
    "Profiles": "profiles",
    "Reports": "reports",
    "Users": "users",
    "WrappedAssets": "wrapped-assets",
}

__all__ = [
    "ENVIRONMENT",
    "CACHE",
    "EXCHANGE",
    "MARKET_DATA",
    "DIRECT_MARKET_DATA",
    "ENDPOINTS"
]
