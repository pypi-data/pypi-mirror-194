# -*- coding: UTF-8 -*-

from dataclasses import dataclass
from decimal import Decimal

from keyring import get_password

from src.cb_exchange_lib import (
    Time,
    Accounts,
    AddressBook,
    CoinbaseAccounts,
    Conversions,
    Currencies,
    Deposits,
    PaymentMethods,
    Transfers,
    Withdrawals,
    Fees,
    Fills,
    Orders,
    Oracle,
    Products,
    Profiles,
    Reports,
    Users,
    WrappedAssets,
)
from src.cb_exchange_lib.constants import EXCHANGE

# ENVIRONMENT: str = "production"
ENVIRONMENT: str = "sandbox"

BTC: dict = {
    "production": "1e682a72-cf29-4752-a391-d90964ab95e5",
    "sandbox": "7e8b32b8-5112-4fa3-a616-8b2b4e5d90ae",
}


@dataclass
class Credentials(object):

    service: str

    @property
    def key(self) -> str:
        return get_password(self.service, "key")

    @property
    def passphrase(self) -> str:
        return get_password(self.service, "passphrase")

    @property
    def secret(self) -> str:
        return get_password(self.service, "secret")

    def as_dict(self) -> dict:
        return {
            "key": self.key,
            "passphrase": self.passphrase,
            "secret": self.secret,
        }


if __name__ == '__main__':

    auth = Credentials(EXCHANGE.get(ENVIRONMENT))

    # ******************** Time: ******************** #

    with Time(environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        time = endpoint.get_time()
        print(time)

    # ******************** Accounts: ******************** #

    with Accounts(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        accounts = endpoint.get_accounts()
        for account in accounts:
            print(account)

        account_id = BTC.get(ENVIRONMENT)

        print("*" * 80)
        account = endpoint.get_account(account_id)
        print(account)

        print("*" * 80)
        holds = endpoint.get_account_holds(account_id, limit=1000)
        print(holds)

        print("*" * 80)
        ledger = endpoint.get_account_ledger(account_id, limit=1000)
        print(ledger)

        print("*" * 80)
        transfers = endpoint.get_account_transfers(account_id, limit=1000)
        print(transfers)

    # ******************** AddressBook: ******************** #

    with AddressBook(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        addresses = endpoint.get_addresses()
        print(addresses)

    # ******************** CoinbaseAccounts: ******************** #

    with CoinbaseAccounts(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        accounts = endpoint.get_wallets()
        print(type(accounts))
        for account in accounts:
            print(account)

        print("*" * 80)
        zero: Decimal = Decimal("0.00000000")
        for account in accounts:
            balance: Decimal = Decimal(account.get("balance"))

            if (balance > zero) or (account.get("currency") in ["RON", "EUR", "USD"]):
                print(account)

        print("*" * 80)
        crypto_address = endpoint.generate_crypto_address("78e6166a-717c-5beb-b095-043601d66f30")
        print(crypto_address)

    # ******************** Conversions: ******************** #

    with Conversions(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        conversion = endpoint.convert_currency(
            from_currency="USD",
            to_currency="USDC",
            amount="50.000000"
        )
        print(conversion)

        print("*" * 80)
        conversion = endpoint.get_conversion(conversion_id=conversion.get("id"))
        print(conversion)

    # ******************** Currencies: ******************** #

    with Currencies(environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        currencies = endpoint.get_currencies()
        for currency in currencies:
            if len(currency.get("convertible_to")) > 0:
                print(currency)

        print("*" * 80)
        currency = endpoint.get_currency(currency_id="BTC")
        print(currency)

    # ******************** PaymentMethods: ******************** #

    with PaymentMethods(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        payment_methods = endpoint.get_payment_methods()
        print(payment_methods)

    # ******************** Transfers: ******************** #

    with Transfers(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        transfers = endpoint.get_transfers()
        for transfer in transfers:
            print(transfer)

        print("*" * 80)
        transfer = endpoint.get_transfer("d6c7cf8d-4453-4cb9-9c63-7fb9dc3180eb")
        print(transfer)

    # ******************** Fees: ******************** #

    print("*" * 80)
    with Fees(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:
        fees = endpoint.get_fees()
        print(fees)

    # ******************** Fills: ******************** #

    with Fills(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        fills = endpoint.get_fills(product_id="BTC-USD")
        print(fills)

    # ******************** Orders: ******************** #

    with Orders(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:
        print("*" * 80)
        orders = endpoint.get_orders(product_id="BTC-USD", limit=100, status=["all", "done", "settled"])
        print(orders)

    # ******************** Oracle: ******************** #

    with Oracle(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        prices = endpoint.get_signed_prices()
        print(prices)

    # ******************** Products: ******************** #

    with Products(environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        products = endpoint.get_products()
        for product in products:
            print(product)

        print("*" * 80)
        product = endpoint.get_product("BTC-USD")
        print(product)

        print("*" * 80)
        book = endpoint.get_product_book("BTC-USD", level=1)
        print(book)

        print("*" * 80)
        candles = endpoint.get_product_candles("BTC-USD", granularity=60)
        for candle in candles:
            print(candle)

        print("*" * 80)
        stats = endpoint.get_product_stats("BTC-USD")
        print(stats)

        print("*" * 80)
        ticker = endpoint.get_product_ticker("BTC-USD")
        print(ticker)

        print("*" * 80)
        trades = endpoint.get_product_trades("BTC-USD")
        print(trades)

    # ******************** Profiles: ******************** #

    with Profiles(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        profiles = endpoint.get_profiles(active=True)
        print(profiles)

        # print("*" * 80)
        # profile = endpoint.create_profile(name="cool_test_profile")
        # print(profile)

    # ******************** Reports: ******************** #

    with Reports(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        reports = endpoint.get_reports()
        print(reports)
        for report in reports:
            print(report)

        print("*" * 80)
        report = endpoint.create_report(
            start_date="2022-01-01T00:00:00.000Z",
            end_date="2022-02-01T00:00:00.000Z",
            balance={"datetime": "2022-02-25T05:00:00.000Z"},
            email="claudiu.drug.87@gmail.com",
            format="csv",
            type="balance",
        )
        print(report)

        print("*" * 80)
        report = endpoint.get_report(report.get("id"))
        print(report)

    # ******************** Users: ******************** #

    with Users(**auth.as_dict(), environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        limits = endpoint.get_exchange_limits(user_id="6128bacb742a52095540a79b")
        print(limits)

    # ******************** WrappedAssets: ******************** #

    with WrappedAssets(environment=ENVIRONMENT) as endpoint:

        print("*" * 80)
        assets = endpoint.get_assets()
        print(assets)
        ids = assets.get("wrapped_assets")
        print(ids)

        print("*" * 80)
        asset_details = endpoint.get_asset_details("CBETH")
        print(asset_details)

        print("*" * 80)
        conversion_rate = endpoint.get_asset_conversion_rate("CBETH")
        print(conversion_rate)
