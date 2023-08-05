# -*- coding: UTF-8 -*-

from abc import ABC
from json import JSONDecodeError
from typing import Union, List, Dict

from requests import Response, HTTPError

from .constants import EXCHANGE, ENDPOINTS, ENVIRONMENT
from .sessions import BaseSession, AuthSession


class Exchange(ABC):
    """Exchange/PRO API base endpoint."""

    _session: Union[BaseSession, AuthSession] = None

    @staticmethod
    def _join(*args, **kwargs) -> str:
        """
        Construct  an url address using `args` for path and `kwargs` as
        query params if given.
        """
        url = "/".join(args)
        if len(kwargs) > 0:
            url = f"{url}?{'&'.join(f'{key}={value}' for key, value in kwargs.items())}"
        return url

    def __init__(self, environment: str):
        """
        :param environment: The API environment (`production` or `sandbox`).
        """
        self._url: str = f"https://{EXCHANGE.get(environment)}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def _get_endpoint_name(self) -> str:
        return ENDPOINTS.get(self.__class__.__name__)

    def close(self):
        """Closes all adapters and as such the session"""
        self._session.close()

    def _get(self, *args, **kwargs):
        return self._request(self._session.get, *args, **kwargs)

    def _post(self, *args, **kwargs):
        return self._request(self._session.post, *args, **kwargs)

    def _delete(self, *args, **kwargs):
        return self._request(self._session.delete, *args, **kwargs)

    def _put(self, *args, **kwargs):
        return self._request(self._session.put, *args, **kwargs)

    def _request(self, method, *args, **kwargs):
        kwargs.update(
            url=self._join(self._url, self._get_endpoint_name(), *args)
        )
        response = method(**kwargs)
        if response.status_code != 200:
            self._raise_for_status(response)
        return response.json()

    def _raise_for_status(self, response: Response):
        try:
            error: dict = response.json()
        except JSONDecodeError:
            response.raise_for_status()
        else:
            status: int = response.status_code
            message: str = error.get("message").rstrip(".?!")
            side: str = self._error_side(status)

            if message is None:
                message: str = response.reason or "Unknown"

            raise HTTPError(
                f"{status} {side} Error: {message}! URL: {response.url}"
            )

    @staticmethod
    def _error_side(status: int) -> str:
        if 400 <= status < 500:
            return "Client"

        if 500 <= status < 600:
            return "Server"


class Endpoint(Exchange):
    """Exchange/PRO API endpoint."""

    def __init__(self, **kwargs):
        """
        **Parameters**:
            - ``environment``: The API environment: `production` or `sandbox`
              (defaults to: `production`);
            - ``retries``: Total number of retries to allow (defaults to: 3);
            - ``backoff``: A backoff factor to apply between attempts after the
              second try (defaults to: 1);
            - ``timeout``: How long to wait for the server to send data before
              giving up (defaults to: 30);
            - ``cache``: Use caching (defaults to: `True`);
            - ``debug``: bool - Set to True to log all requests/responses
              to/from server (defaults to: `False`);
            - ``logger``: Logger - The handler to be used for logging.
              If given, and level is above `DEBUG`, all debug messages will be
              ignored.
        """
        super(Endpoint, self).__init__(
            environment=kwargs.pop("environment", ENVIRONMENT)
        )
        self._session = BaseSession(**kwargs)


class AuthEndpoint(Exchange):
    """Exchange/Pro API authenticated endpoint."""

    def __init__(self, key: str, passphrase: str, secret: str, **kwargs):
        """
        **Parameters**:
            - ``key``: The API key;
            - ``passphrase``: The API passphrase;
            - ``secret``: The API secret;
            - ``environment``: The API environment: `production` or `sandbox`
              (defaults to: `production`);
            - ``retries``: Total number of retries to allow (defaults to: 3);
            - ``backoff``: A backoff factor to apply between attempts after the
              second try (defaults to: 1);
            - ``timeout``: How long to wait for the server to send data before
              giving up (defaults to: 30);
            - ``cache``: Use caching (defaults to: `True`);
            - ``debug``: bool - Set to True to log all requests/responses
              to/from server (defaults to: `False`);
            - ``logger``: Logger - The handler to be used for logging.
              If given, and level is above `DEBUG`, all debug messages will be
              ignored.
        """
        super(AuthEndpoint, self).__init__(
            environment=kwargs.pop("environment", ENVIRONMENT)
        )
        self._session = AuthSession(key, passphrase, secret, **kwargs)


class Time(Endpoint):
    """`time` endpoint of Exchange/Pro API."""

    def get_time(self) -> Dict:
        """Get the API server time."""
        return self._get()


class Accounts(AuthEndpoint):
    """
    `accounts` endpoint of the Exchange/Pro API.

    ----

    **INFO**
    Your trading accounts are separate from your Coinbase accounts.
    See Deposit from Coinbase account for documentation on how to
    deposit funds to begin trading.

    ----

    **API Key Permissions**
    This endpoint requires either the ``view`` or ``trade`` permission.

    ----

    **Rate Limits**
    This endpoint has a custom rate limit by profile ID:
        - 25 requests per second
        - 50 requests per second in bursts

    ----

    **Funds on Hold**
    When you place an order, the funds for the order are placed on hold.
    They cannot be used for other orders or withdrawn.
    Funds will remain on hold until the order is filled or canceled.
    """

    def get_accounts(self) -> List:
        """
        Get a list of trading accounts from the profile of the API key.
        """
        return self._get()

    def get_account(self, account_id: str) -> Dict:
        """
        Information for a single account.
        Use this endpoint when you know the account_id.
        API key must belong to the same profile as the account.

        :param account_id: The ID of the trading account.
        """
        return self._get(account_id)

    def get_account_holds(self, account_id: str, **kwargs) -> List:
        """
        List the holds of an account that belong to the same profile as the
        API key. Holds are placed on an account for any active orders or
        pending withdraw requests. As an order is filled, the hold amount is
        updated. If an order is canceled, any remaining hold is removed.
        For withdrawals, the hold is removed after it is completed.

        **kwargs:**
            - ``before``: str - Used for pagination. Sets start cursor to
              before date.
            - ``after``: str - Used for pagination. Sets end cursor to
              after date.
            - ``limit``: int - Limit on number of results to return.

        :param account_id: The ID of the trading account.
        :param kwargs: Additional keyword arguments.
        """

        if "limit" not in kwargs:
            kwargs.update(limit=100)

        return self._get(account_id, "holds", params=kwargs)

    def get_account_ledger(self, account_id: str, **kwargs) -> List:
        """
        Lists ledger activity for an account. This includes anything that
        would affect the accounts balance - transfers, trades, fees, etc.
        List account activity of the API key's profile. Account activity
        either increases or decreases your account balance.

        **kwargs:**
            - ``start_date``: str - Filter results by minimum posted date.
            - ``end_date``: str - Filter results by maximum posted date.
            - ``before``: str - Used for pagination. Sets start cursor to
              before date.
            - ``after``: str - Used for pagination. Sets end cursor to after
              date.
            - ``limit``: int - Limit on number of results to return.
            - ``profile_id``: str

        :param account_id: The ID of the trading account.
        :param kwargs:  Additional keyword arguments.
        """

        if "limit" not in kwargs:
            kwargs.update(limit=100)

        return self._get(account_id, "ledger", params=kwargs)

    def get_account_transfers(self, account_id: str, **kwargs) -> List:
        """
        Lists past withdrawals and deposits for an account.

        **kwargs:*
            - ``before``: str - Used for pagination. Sets start cursor to before date.
            - ``after``: str - Used for pagination. Sets end cursor to after date.
            - ``limit``: int - Limit on number of results to return.
            - ``type``: str

        :param account_id: The ID of the trading account.
        :param kwargs:  Additional keyword arguments.
        """

        if "limit" not in kwargs:
            kwargs.update(limit=100)

        return self._get(account_id, "transfers", params=kwargs)


class AddressBook(AuthEndpoint):
    """`address-book` endpoint of the Exchange/Pro API."""

    def get_addresses(self) -> List:
        """Get all addresses stored in the address book."""
        return self._get()


class CoinbaseAccounts(AuthEndpoint):
    """`coinbase-accounts` endpoint of the Exchange/Pro API."""

    def get_wallets(self) -> List:
        """
        Gets all the user's available Coinbase wallets (These are the
        wallets/accounts that are used for buying and selling on
        www.coinbase.com).
        """
        return self._get()

    def generate_crypto_address(self, account_id: str, **kwargs) -> Dict:
        """
        Generates a one-time crypto address for depositing crypto.

        **INFO:**
        You can generate an address for crypto deposits.
        See the Coinbase Accounts section for information on how to retrieve
        your coinbase account ID.

        **kwargs:**
            - account_id: str
            - profile_id: str
            - network: str

        :param account_id: Coinbase account ID.
        :param kwargs: Additional keyword arguments.
        """
        return self._post(account_id, "addresses", json=kwargs)


class Conversions(AuthEndpoint):
    """
    `conversions` endpoint of the Exchange/Pro API.

    **CAUTION:**
    Users whose `USD` and `USDC` accounts are unified do not have access to the
    conversion endpoint, and conversions from `USDC` to `USD` are automatic upon
    deposit.
    """

    def convert_currency(self, from_currency: str, to_currency: str, amount: str, **kwargs) -> Dict:
        """

        Converts funds from `from` currency to `to` currency.
        Funds are converted on the `from` account in the `profile_id` profile.

        **RESPONSE:**
        A successful conversion is assigned a conversion ID. The corresponding
        ledger entries for a conversion reference this conversion ID.

        **kwargs:**
            - ``profile_id``: str
            - ``nonce``: str

        :param from_currency: Currency account (i.e. `USD`).
        :param to_currency: Currency account (i.e. `USDC`).
        :param amount: Amount to be converted.
        :param kwargs: Additional keyword arguments.
        """
        kwargs.update(
            {
                "from": from_currency,
                "to": to_currency,
                "amount": amount,
            }
        )
        return self._post(json=kwargs)

    def get_conversion(self, conversion_id: str, **kwargs) -> Dict:
        """
        Gets a currency conversion by id
        (i.e. `41554f00-5c34-4f09-b800-2a878e52f2ea`).

        **kwargs:**
            - ``profile_id``: str

        :param conversion_id: The conversion ID.
        :param kwargs: Additional keyword arguments.
        """
        return self._get(conversion_id, params=kwargs)


class Currencies(Endpoint):
    """
    `currencies` endpoint of the Exchange/Pro API.

    **INFO:**
    Not all currencies may be currently in use for trading.
    """

    def get_currencies(self) -> List:
        """
        Gets a list of all known currencies.

        Note:
            Not all currencies may be currently in use for trading.
        """
        return self._get()

    def get_currency(self, currency_id: str) -> Dict:
        """
        Gets a single currency by ID (i.e. `BTC`).

        Currency codes conform to the ISO 4217 standard where possible.
        Currencies that have no representation in ISO 4217 can use a
        custom code.

        :param currency_id: `ISO 4217` standard ID or custom code.
        """
        return self._get(currency_id)


class Deposits(AuthEndpoint):
    """
    `deposits` endpoint of the Exchange/Pro API.

    **DEPOSIT FUNDS FROM A COINBASE ACCOUNT:**
    You can move funds between your Coinbase accounts and your Coinbase
    Exchange trading accounts within your daily limits. Moving funds between
    Coinbase and Coinbase Exchange is instant and free.
    See the :class:`CoinbaseAccounts` section for retrieving your
    Coinbase accounts.
    """

    def deposit_from_coinbase_account(
            self,
            account_id: str,
            currency: str,
            amount: str,
            **kwargs
    ) -> Dict:
        """
        Deposits funds from a https://www.coinbase.com wallet to the specified
        `profile_id`.

        **kwargs:**
            - ``profile_id``: str - Coinbase Exchange trading account ID.

        :param amount: Amount to be transferred.
        :param account_id: Coinbase account ID
        :param currency: Currency to be transferred.
        """
        kwargs.update(
            coinbase_account_id=account_id,
            currency=currency,
            amount=amount,
        )
        return self._post("coinbase-account", json=kwargs)

    def deposit_from_payment_method(
            self,
            method_id: str,
            currency: str,
            amount: str,
            **kwargs
    ) -> Dict:
        """
        Deposits funds from a linked external payment method to the
        specified `profile_id`.

        **kwargs:**
            - ``profile_id``: str - Coinbase Exchange trading account ID.

        :param amount: Amount to be transferred.
        :param method_id: Linked external payment method ID.
        :param currency: Currency to be transferred.
        """
        kwargs.update(
            amount=amount,
            payment_method_id=method_id,
            currency=currency,
        )
        return self._post("payment-method", json=kwargs)


class PaymentMethods(AuthEndpoint):
    """`payment-methods` endpoint of the Exchange/Pro API."""

    def get_payment_methods(self) -> List:
        """Gets a list of the user's linked payment methods."""
        return self._get()


class Transfers(AuthEndpoint):
    """
    `transfers` endpoint of the Exchange/Pro API.
    """

    def get_transfers(self, **kwargs) -> List:
        """
        Gets a list of in-progress and completed transfers of funds in/out of
        the user's accounts.

        **Parameters:**
            - ``profile_id``: str - Returns list of transfers from this portfolio id.
            - ``before``: str - Used for pagination. Sets start cursor to before date.
            - ``after``: str - Used for pagination. Sets end cursor to after date.
            - ``limit``: int - Limit on number of results to return.
            - ``type``: str - Specify transfers 'deposit' or 'withdraw'.
        """
        return self._get(params=kwargs)

    def get_transfer(self, transfer_id: str) -> Dict:
        """
        Get information on a single transfer.

        :param transfer_id: The transfer ID.
        """
        return self._get(transfer_id)


class Withdrawals(AuthEndpoint):
    """
    `withdrawals` endpoint of the Exchange/Pro API.

    You can move funds between your Coinbase accounts and your
    Coinbase Exchange trading accounts within your daily limits.
    Moving funds between Coinbase and Coinbase Exchange is instant and free.
    See the :class:`CoinbaseAccounts` section for retrieving your Coinbase
    accounts.
    """

    def withdraw_to_coinbase_account(
            self,
            account_id: str,
            currency: str,
            amount: str,
            **kwargs
    ) -> Dict:
        """
        Withdraws funds from the specified `profile_id` to a
        https://www.coinbase.com wallet.

        **kwargs:**
            - ``profile_id``: str - Coinbase Exchange trading account ID.

        :param amount: Amount to be transferred.
        :param account_id: Coinbase account ID
        :param currency: Currency to be transferred.
        :param kwargs: Additional keyword arguments.
        """
        kwargs.update(
            amount=amount,
            coinbase_account_id=account_id,
            currency=currency,
        )
        return self._post("coinbase-account", json=kwargs)

    def withdraw_to_crypto_address(
            self,
            crypto_address: str,
            currency: str,
            amount: str,
            **kwargs
    ) -> Dict:
        """
        Withdraws funds from the specified `profile_id` to an external crypto
        address.

        **NOTE:**
            The network parameter was added to support multichain withdrawals,
            but is only applicable for ETH, MATIC, and USDC on Polygon, and
            USDC on Solana.
            Verify the list of supported networks per currency via the
            :class:`Currencies` endpoint.
            If you are transferring any crypto via the default network
            (e.g. USDT, this is the Ethereum network), then you do not need to
            use the network parameter in your call.

        **kwargs:**
            - ``profile_id``: str
            - ``destination_tag``: str
            - ``no_destination_tag``: bool
            - ``two_factor_code``: str
            - ``nonce``: int
            - ``network``: str - Network for multichain withdrawals.
            - ``add_network_fee_to_total``: bool - A boolean flag to add the
              network fee on top of the amount. If this is blank, it will
              default to deducting the network fee from the amount.

        :param amount: Amount to be transferred.
        :param currency: Currency to be transferred.
        :param crypto_address: External crypto address.
        :param kwargs: Additional keyword arguments.
        """
        kwargs.update(
            amount=amount,
            currency=currency,
            crypto_address=crypto_address,
        )
        return self._post("crypto", json=kwargs)

    def get_fee_estimate(self, currency: str, crypto_address: str, **kwargs) -> Dict:
        """
        Gets the fee estimate for the crypto withdrawal to crypto address.

        **kwargs:**
            - `network`: str

        :param currency:
        :param crypto_address:
        :param kwargs: Additional keyword arguments.
        """
        kwargs.update(
            currency=currency,
            crypto_address=crypto_address,
        )
        return self._get("fee-estimate", params=kwargs)

    def withdraw_to_payment_method(
            self,
            method_id: str,
            currency: str,
            amount: str,
            **kwargs
    ) -> Dict:
        """
        Withdraws funds from the specified `profile_id` to a linked external
        payment method.

        **WITHDRAW FUNDS TO A PAYMENT METHOD:**
            See the :class:`PaymentMethods` section for retrieving your payment
            methods.

        **kwargs:**
            - profile_id: str

        :param amount:
        :param method_id:
        :param currency:
        :param kwargs: Additional keyword arguments.
        """
        kwargs.update(
            amount=amount,
            payment_method_id=method_id,
            currency=currency,
        )
        return self._post("payment-method", json=kwargs)


class Fees(AuthEndpoint):
    """`fees` endpoint of the Exchange/Pro API."""

    def get_fees(self) -> Dict:
        """
        Get fees rates and 30 days trailing volume.

        This request returns your current maker & taker fee rates, as well as
        your 30-day trailing volume. Quoted rates are subject to change.

        For more information, see:
            https://help.coinbase.com/en/pro/trading-and-funding/trading-rules-and-fees/fees.html
        """
        return self._get()


class Fills(AuthEndpoint):
    """`fills` endpoint of the Exchange/Pro API."""

    def get_fills(self, **kwargs) -> List:
        """
        Get a list of fills.
        A fill is a partial or complete match on a specific order.
        Get a list of recent fills of the API key's profile.

        **Settlement and Fees:**
            Fees are recorded in two stages. Immediately after the matching
            engine completes a match, the fill is inserted into our datastore.
            Once the fill is recorded, a settlement process settles the fill
            and credit both trading counterparties.

            The `fee` field indicates the fees charged for this individual fill.

        **Liquidity:**
            The `liquidity` field indicates if the fill was the result of a
            liquidity provider or liquidity taker. `M` indicates Maker and `T`
            indicates Taker.

        **Pagination:**
            Fills are returned sorted by descending `trade_id` from the largest
            `trade_id` to the smallest `trade_id`.
            The `CB-BEFORE` header has this first trade ID so that future
            requests using the `cb-before` parameter fetch fills with a greater
            trade ID (newer fills).

            See https://docs.cloud.coinbase.com/exchange/docs/pagination for
            more information.

        **kwargs:**
            - ``order_id``: Limit to fills on a specific order.
              Either `order_id` or `product_id` is required.
            - ``product_id``: Limit to fills on a specific product.
              Either `order_id` or `product_id` is required.
            - ``profile_id``: Get results for a specific profile
            - ``limit``: Limit on number of results to return.
            - ``before``: Used for pagination. Sets start cursor to
              `before` date.
            - ``after``: Used for pagination. Sets end cursor to `after` date.
            - ``market_type``: Market type which the order was filled in.
        """
        return self._get(params=kwargs)


class Orders(AuthEndpoint):
    """
    `orders` endpoint of the Exchange/Pro API.
    """

    def get_orders(self, **kwargs) -> List:
        """
        List your current open orders. Only open or un-settled orders are
        returned by default. As soon as an order is no longer open and settled,
        it will no longer appear in the default request. Open orders may change
        state between the request and the response depending on market
        conditions.

        **kwargs:**
            - ``profile_id``: str - Filter results by a specific `profile_id`.
            - ``product_id``: str - Filter results by a specific `product_id`.
            - ``sortedBy``: str - Sort criteria for results.
            - ``sorting``: str - Ascending or descending order, by sortedBy.
            - ``start_date``: str - Filter results by minimum posted date.
            - ``end_date``: str - Filter results by maximum posted date.
            - ``before``: str - Used for pagination. Sets start cursor to before date.
            - ``after``: str - Used for pagination. Sets end cursor to after date.
            - ``limit``: int - Limit on number of results to return.
            - ``status``: List[str] - Array with order statuses to filter by.
            - ``market_type``: str - Market type which the order was traded in.
        """
        return self._get(params=kwargs)

    def create_order(self, **kwargs) -> Dict:
        """
        Create an order.
        You can place two types of orders: limit and market.
        Orders can only be placed if your account has sufficient funds.
        Once an order is placed, your account funds will be put on hold for
        the duration of the order. How much and which funds are put on hold
        depends on the order type and parameters specified.

        **kwargs:**
            - ``profile_id``: str - Create order on a specific profile_id.
              If none is passed, defaults to default profile.
            - ``type``: str - Possible values: [limit, market, stop]
            - ``side``: str - Possible values: [buy, sell]
            - ``product_id``: str - Book on which to place an order
            - ``stp``: str - Possible values: [dc, co, cn, cb]
            - ``stop``: str - Possible values: [loss, entry]
            - ``stop_price``: str - Price threshold at which a stop order will
              be placed on the book
            - ``price``: str - Price per unit of cryptocurrency - required for
              limit/stop orders
            - ``size``: str - Amount of base currency to buy or sell - required
              for limit/stop orders and market sells
            - ``funds``: str - Amount of quote currency to buy - required for
               market buys
            - ``time_in_force``: str - Possible values: [GTC, GTT, IOC, FOK]
            - ``cancel_after``: str - Possible values: [min, hour, day]
            - ``post_only``: bool - If true, order will only execute as a
              maker order
            - ``client_oid``: str - Optional Order ID selected by the user or
              the frontend client to identify their order
        """
        return self._post(json=kwargs)

    def del_orders(self, **kwargs) -> Dict:
        """
        With best effort, cancel all open orders.
        This may require you to make the request multiple times until all
        of the open orders are deleted.

        **kwargs:**
            - profile_id: str - Cancels orders on a specific profile.
            - product_id: str - Cancels orders on a specific product only.
        """
        return self._delete(params=kwargs)

    def get_order(self, order_id: str, **kwargs) -> Dict:
        """
        Get a single order by id.

        **NOTE:**
            Orders can be queried using either the exchange assigned id or the
            client assigned client_oid. When using client_oid it must be
            preceded by the client: namespace. If the order is canceled,
            and if the order had no matches, the response might return the
            status code 404.

        **kwargs:**
            - ``market_type``: str - Market type which the order was traded in.

        :param order_id: `order_id` is either the exchange assigned id or the
            client assigned `client_oid`. When using `client_oid` it must be
            preceded by the client: namespace.
        :param kwargs: Additional keyword arguments.
        """
        return self._get(order_id, params=kwargs)

    def del_order(self, order_id: str, **kwargs) -> Dict:
        """
        Cancel a single open order by `order_id`.

        **CANCEL A PREVIOUSLY PLACED ORDER:**
            The order must belong to the profile that the API key belongs to.
            If the order had no matches during its lifetime, its record may
            be purged. This means the order details is not available with
            ``GET /orders/{order_id}``.

        **CAUTION:**
            To prevent a race condition when canceling an order, it is highly
            recommended that you specify the product id as a query string.

        **NOTE:**
            Orders can be canceled using either the exchange assigned id or
            the client assigned client_oid. When using client_oid it must be
            preceded by the client: namespace.

        **Response:**
            A successfully cancelled order response includes:

                - the order ID if the order is cancelled with the exchange
                  assigned id,
                - the client assigned client_oid if the order is cancelled
                  with client order ID.

        **Cancel Reject:**
            If the order could not be canceled (already filled or previously
            canceled, etc.), then an error response indicates the reason in
            the message field.

        **kwargs:**
            - profile_id: str - Cancels orders on a specific profile
            - product_id: str - Optional product id of order

        :param order_id: Orders may be canceled using either the exchange
            assigned id or the client assigned `client_oid`. When using
            `client_oid` it must be preceded by the client: namespace.
        :param kwargs: Additional keyword arguments.
        """
        return self._delete(order_id, params=kwargs)


class Oracle(AuthEndpoint):
    """
    `oracle` endpoint of the Exchange/Pro API.
    """

    def get_signed_prices(self) -> Dict:
        """
        Get cryptographically signed prices ready to be posted on-chain using
        Compound's Open Oracle smart contract.
        """
        return self._get()


class Products(Endpoint):
    """
    `products` endpoint of the Exchange/Pro API.
    """

    def get_products(self, **kwargs) -> List:
        """
        Gets a list of available currency pairs for trading.

        **ORDER SIZE LIMITS REMOVED:**
            The properties `base_max_size`, `base_min_size`, `max_market_funds`
            were removed on June 30.

            The property, `min_market_funds`, has been repurposed as the
            notional minimum size for limit orders.

        The `base_min_size` and `base_max_size` fields define the min and
        max order size.

        The `min_market_funds` and `max_market_funds` fields define the
        min and max funds allowed in a market order.

        `status_message` provides any extra information regarding the
        status if available.

        The `quote_increment` field specifies the min order price as well as
        the price increment.

        The order price must be a multiple of this increment (i.e. if the
        increment is 0.01, order prices of 0.001 or 0.021 would be rejected).

        The `base_increment` field specifies the minimum increment for the
        `base_currency`.

        `trading_disabled` indicates whether trading is currently restricted
        on this product, this includes whether both new orders and order
        cancelations are restricted.

        `cancel_only` indicates whether this product only accepts cancel
        requests for orders.

        `post_only` indicates whether only maker orders can be placed.
        No orders will be matched when post_only mode is active.

        `limit_only` indicates whether this product only accepts limit orders.

        Only a maximum of one of `trading_disabled`, `cancel_only`,
        `post_only`, `limit_only` can be true at once. If none are true,
        the product is trading normally.

        `fx_stablecoin` indicates whether the currency pair is a Stable Pair.

        `auction_mode` boolean which indicates whether or not the book is in
        auction mode. For more details on the auction mode
        see `get_product_book()` describing the level 1 book which contains
        information pertaining to products in auction mode.

        INFO
            When `limit_only` is true, matching can occur if a limit order
            crosses the book. Product ID will not change once assigned to
            a product but all other fields ares subject to change.

        **kwargs:**
            - ``type``: str

        """
        return self._get(params=kwargs)

    def get_product(self, product_id: str) -> Dict:
        """Get information on a single product."""
        return self._get(product_id)

    def get_product_book(self, product_id: str, **kwargs) -> Dict:
        """
        Get a list of open orders for a product.
        The amount of detail shown can be customized with the `level` parameter.

        **Details:**
            By default, only the inside (i.e., the best) bid and ask are
            returned. This is equivalent to a book depth of 1 level. To see a
            larger order book, specify the level query parameter.

            If a level is not aggregated, all of the orders at each price are
            returned. Aggregated levels return only one size for each active
            price (as if there was only a single order for that size at the
            level).

        **Levels:**
            - 1: The best bid, ask and auction info
            - 2: Full order book (aggregated) and auction info
            - 3: Full order book (non aggregated) and auction info

        **Levels 1 and 2 are aggregated.**
        The size field is the sum of the size of the orders at that price,
        and num-orders is the count of orders at that price; size should
        not be multiplied by num-orders.

        **Level 3 is non-aggregated** and returns the entire order book.

        **Auction Mode**
            While the book is in an auction, the L1, L2 and L3 book contain
            the most recent indicative quote disseminated during the auction,
            and `auction_mode` is set to true.

            These indicative quote messages are sent on an interval basis
            (approximately once a second) during the collection phase of an
            auction and includes information about the tentative price and
            size affiliated with the completion.

                - ``Opening Price`` - The price used for matching all the
                  orders as the auction enters the opening state.

                - ``Opening Size`` - Aggregate size of all the orders eligible
                  for crossing Best Bid/Ask Price and Size.
                  The anticipated BBO upon entering trading after matching has
                  completed.

            Because these indicative quote messages get disseminated on an
            interval basis, the values aren’t firm as changes in the book may
            occur between the last update and beginning the transition from
            auction mode to trading.

            While in auction mode, the `auction_state` indicates what phase the
            auction is in which includes:
                - ``collection``
                - ``opening``
                - ``complete``


        **Auction Details**
        The `collection` state indicates the auction is currently accepting
        orders and cancellations within the book. During this state, orders do
        not match and the book may appear crossed in the market data feeds.

        The `opening` state indicates the book transitions towards full
        trading or limit only. During `opening` state any buy orders at or
        over the open price and any sell orders at or below the open price
        may cross during the opening phase. Matches in this stage are
        charged taker fees. Any new orders or cancels entered while in the
        opening phase get queued and processed when the market resumes trading.

        The `complete` state indicates the dissemination of opening trades is
        finishing, and immediately after that the book goes into the next mode
        (either full trading or limit only).

        The `opening` state passes by too quickly in most normal scenarios to
        see these states show up in the REST API.

        During the `collection` state the `can_open` field indicates whether
        or not the book can complete the auction and enter full trading or
        limit only mode.

        `can_open: yes` indicates the book is in a healthy state and the book
        can enter full trading or limit only once the auction collection state
        finishes.

        `can_open: no` indicates the book cannot continue to full trading or
        limit only.

        Once a book leaves auction mode — either by moving to full trading, or
        by being canceled by our market ops team — the book endpoint no longer
        shows indicative quote data and display `auction_mode` as false.

        **INFO**
            This request is NOT paginated. The entire book is returned in one
            response.

        **INFO**
            Level 1 and Level 2 are recommended for polling. For the most
            up-to-date data, consider using the WebSocket stream. Level 3 is
            only recommended for users wishing to maintain a full real-time
            order book using the WebSocket stream. Abuse of Level 3 via
            polling can cause your access to be limited or blocked.

        **kwargs:**
            - level: int

        :param product_id:
        """
        return self._get(product_id, "book", params=kwargs)

    def get_product_candles(self, product_id: str, **kwargs) -> List[List]:
        """
        Historic rates for a product.
        Rates are returned in grouped buckets.

        Candle schema is of the form:
            `[timestamp, price_low, price_high, price_open, price_close]`

        **INFO**
            Historical rate data may be incomplete. No data is published for
            intervals where there are no ticks. Historical rates should not
            be polled frequently. If you need real-time information,
            use the trade and book endpoints along with the WebSocket feed.

        **Details**
            If the `start` or `end` field is not provided, then both fields are
            ignored. If a custom time range is not declared then one ending
            now is selected.

            The `granularity` field must be one of the following values:
            `{60, 300, 900, 3600, 21600, 86400}`. Otherwise, your request will
            be rejected. These values correspond to timeslices representing:
                - ``one minute``
                - ``five minutes``
                - ``fifteen minutes``
                - ``one hour``
                - ``six hours``
                - ``one day``

            If data points are readily available, your response may contain as
            many as 300 candles and some of those candles may precede your
            declared `start` value. The maximum number of data points for a
            single request is 300 candles. If your selection of start/end time
            and granularity results in more than 300 data points, your request
            will be rejected. If you wish to retrieve fine granularity data
            over a larger time range, you must make multiple requests with new
            start/end ranges.

        **Response Items**
            Each bucket is an array of the following information:

                - ``time``: Bucket start time
                - ``low``: Lowest price during the bucket interval
                - ``high``: Highest price during the bucket interval
                - ``open``: Opening price (first trade) in the bucket interval
                - ``close``: Closing price (last trade) in the bucket interval
                - ``volume``: Volume of trading activity during the bucket
                  interval

        **kwargs:**
            - ``granularity``: str - one of the following values:
                - `60`: one minute
                - `300`: five minutes
                - `900`: fifteen minutes
                - `3600`: one hour
                - `21600`: six hours
                - `86400`: one day
            - ``start``: str - Timestamp for starting range of aggregations
            - ``end``: str - Timestamp for ending range of aggregations

        :param product_id: The product ID (i.e. `BTC-USD`)
        :param kwargs: Additional keyword arguments.
        """
        return self._get(product_id, "candles", params=kwargs)

    def get_product_stats(self, product_id: str) -> Dict:
        """
        Gets 30day and 24hour stats for a product.

        INFO
            The `volume` property is in base currency units.
            Properties `open`, `high`, `low` are in quote currency units.

        :param product_id: The product ID (i.e. `BTC-USD`)
        """
        return self._get(product_id, "stats")

    def get_product_ticker(self, product_id: str) -> Dict:
        """
        Gets snapshot information about the last trade (tick),
        best bid/ask and 24h volume.

        **Real-time updates**
            Coinbase recommends that you get real-time updates by connecting
            with the WebSocket stream and listening for match messages,
            rather than polling.

        :param product_id: The product ID (i.e. `BTC-USD`)
        """
        return self._get(product_id, "ticker")

    def get_product_trades(self, product_id: str, **kwargs) -> List[Dict]:
        """
        Gets a list the latest trades for a product.

        **Side**
            The `side` of a trade indicates the maker order side.
            The maker order is the order that was open on the order book.

            A `buy` side indicates a down-tick because the maker was a buy
            order and their order was removed. A `sell` side indicates an
            up-tick.

        **kwargs:**
            - ``limit``: int
            - ``before``: int
            - ``after``: int

        :param product_id: The product ID (i.e. `BTC-USD`)
        :param kwargs: Additional keyword arguments.
        """
        return self._get(product_id, "trades", params=kwargs)


class Profiles(AuthEndpoint):
    """
    `profiles` endpoint of the Exchange/Pro API.
    """

    def get_profiles(self, **kwargs) -> List[Dict]:
        """
        Gets a list of all of the current user's profiles.

        **kwargs:**
            - ``active``: bool

        :param kwargs: Additional keyword arguments.
        """
        if ("active" in kwargs) and isinstance(kwargs.get("active"), bool):
            kwargs.update(
                active=str(kwargs.get("active")).lower()
            )
        return self._get(params=kwargs)

    def create_profile(self, name: str) -> Dict:
        """
        Create a new profile.
        Will fail if no name is provided or if user already has max number of
        profiles.

        :param name: Profile name.
        """
        return self._post(
            json={"name": name}
        )

    def transfer_funds(self, from_profile: str, to_profile: str, currency: str, amount: str) -> Dict:
        """
        Transfer an amount of currency from one profile to another.
        """
        return self._post(
            "transfer",
            json={
                "from": from_profile,
                "to": to_profile,
                "currency": currency,
                "amount": amount,
            }
        )

    def get_profile(self, profile_id: str, **kwargs) -> Dict:
        """
        Information for a single profile.
        Use this endpoint when you know the `profile_id`.

        :param profile_id: Profile ID.
        :param kwargs: Additional keyword arguments.
        """
        if ("active" in kwargs) and isinstance(kwargs.get("active"), bool):
            kwargs.update(
                active=str(kwargs.get("active")).lower()
            )
        return self._get(profile_id, params=kwargs)

    def rename_profile(self, profile_id: str, **kwargs) -> Dict:
        """
        Rename a profile. Names 'default' and 'margin' are reserved.

        **kwargs:**
            - ``profile_id``: str - ?
            - ``name``: str

        :param profile_id: Profile ID.
        :param kwargs: Additional keyword arguments.
        """
        return self._put(profile_id, json=kwargs)

    def del_profile(self, profile_id: str, **kwargs) -> Dict:
        """
        Deletes the profile specified by `profile_id` and transfers all funds
        to the profile specified by `to`. Fails if there are any open orders
        on the profile to be deleted.

        **kwargs:**
            - ``profile_id``: str - ?
            - ``to``: str

        :param profile_id: Profile ID.
        :param kwargs: Additional keyword arguments.
        """
        return self._put(profile_id, "deactivate", json=kwargs)


class Reports(AuthEndpoint):
    """`reports` endpoint of the Exchange/Pro API."""

    def get_reports(self, **kwargs) -> List[Dict]:
        """
        Gets a list of all user generated reports.

        **INFO**
            Once a report request has been accepted for processing, you can
            poll the report resource endpoint at `/reports/{report_id}` for its
            status. When status is `ready`, the final report is uploaded and
            available at `{file_url}`.

        Parameters:
            - ``profile_id``: str - Filter results by a specific `profile_id`.
            - ``after``: str - Filter results after a specific date.
            - ``limit``: int - Limit results to a specific number.
            - ``type``: str
              Filter results by type of report:
                - fills
                - account
                - balance
                - otc-fills
                - 1099k-transaction-history
                - tax-invoice
            - ``ignore_expired``: bool - Ignore expired results

        :param kwargs: Additional keyword arguments.
        """
        return self._get(params=kwargs)

    def create_report(self, **kwargs) -> Dict:
        """
        Generates a report.
        You can create reports with historical data for all report types.
        Balance reports can be snapshots of historical or current data.
        Reports provide batches of historic information about your profile in
        various human and machine readable forms.

        **INFO**
            A report is generated when resources are available. You can poll
            the report resource endpoint at `/reports/{report_id}` for its
            status. When status is `ready`, the final report is uploaded and
            available at `{file_url}`.

        **Expired reports**
            Reports are only available for download for a few days after being
            created. Once a report expires, the report is no longer available
            for download and is deleted.

        **Balance Reports**
            Balance statements represent historical or current point-in-time
            `snapshots` in native and fiat converted units.

            Balance statement reports:

                - Can be generated for a specific portfolio (API and UI) or
                  all portfolios (UI only). In the UI, all portfolios can be
                  grouped by portfolio or asset (with balances totaled across
                  portfolios).

                - Include balances for crypto and fiat assets supported on the
                  Exchange (USD, EUR, GBP).

                - Include balances in both native units (e.g., 1 BTC) as well
                  as fiat-converted units assets (e.g., $20000 USD worth of
                  BTC) where price data is available.

                - Are generated for all assets (crypto and fiat) in the user’s
                  account as of the requested timestamp. They cannot be
                  generated for a specific asset (as is possible with the
                  account and fill reports).

        **CAUTION**
            API calls are tied to a specific portfolio but you can group by
            all portfolios in the UI.

        **Timestamps**
            - ``Range``: Timestamps are UTC-exclusive. For example, to
              generate a balance as of December 31st, 2022 EOD UTC
              (11:59:59 PM UTC), input January 1st, 2023 12:00:00 AM UTC.

            - ``Granularity``: The API is the most granular and lets you
              specify a timestamp to the very second. The UI lets you specify
              the day and hour.

        **Fiat Conversion**
            **For fiat balances** (USD, EUR, GBP), the conversion price is 1:1
            and is reported in that specific fiat currency. EUR/GBP is not
            converted to USD balance.

            **For crypto balances** the conversion price is the volume weighted
            average of closing prices in USD (when available). It is calculated
            by fetching 1 hour candles between [t-24 hours to t] and taking a
            volume weighted average of the closing price of the candles
            (when available).

                - Requested timestamp = t; Start range = t - 24 hours;
                  End range = t;

                - Candles may not be available; e.g., delisted assets may not
                  have candles at the requested timestamp.

                - If a USD pair is not listed for trading at the requested
                  timestamp, fiat conversion is not possible.

        **Request Details**

            The Balance Report API:

                - Leverages the existing /reports endpoint.

                - Adds a new report type of balance.

                - Adds a balance object to the request with datetime (and
                  `group_by_potfolio_id` for the UI only).

                - Keeps the same response schema (with the possibility that
                  "type"="balance").

        **kwargs:**
            - ``start_date``: str - Start date for items to be included in
              report.

            - ``end_date``: str - End date for items to be included in report.

            - ``type``: str

                Possible values:
                    - ``fills``
                    - ``account``
                    - ``otc-fills``
                    - ``1099k-transaction-history``
                    - ``tax-invoice``
                    - ``balance``
                    - ``rfq-fills``

            - ``year``: str - required for `1099k-transaction-history-type`
              reports.

            - ``format``: str

                Possible values:
                    - ``pdf``
                    - ``csv``

            - ``product_id``: str - Product - required for `fills`-type
              reports.

            - ``account_id``: str - Account - required for `account`-type
              reports.

            - ``email``: str - Email to send generated report notification to

            - ``profile_id``: str - If this field is specified, it must be the
              profile_id that is linked to the API key.


            - ``balance``: dict

                - ``datetime``: str - Designated date and time of the balance
                  statement. Timezone is always UTC. If this field is empty, a
                  report of the user’s current balance will be generated.

                - ``group_by_profile``: bool - Not applicable if generating
                  report through an API key; only available through report
                  generation via the Exchange user interface (UI).


            - ``fills``: dict

                - ``start_date``: str - Start date for items to be included in
                  report.

                - ``end_date``: str - End date for items to be included in
                  report.

                - ``product_id``: str - Product - Which product to generate
                  the report for.

            - ``account``: dict

                - ``start_date``: str - Start date for items to be included in
                  report.

                - ``end_date``: str - End date for items to be included in
                  report.

                - ``account_id``: str - Account - Which account to generate
                  the report for.

            - ``otc-fills``: dict

                - start_date: str - Start date for items to be included in
                  report.

                - end_date: str - End date for items to be included in report.

                - product_id: str - Product - Which product to generate the
                  report for.

            - ``tax-invoice``: dict

                - ``start_date``: str - Start date for items to be included in
                  report.

                - ``end_date``: str - End date for items to be included in
                  report.

                - ``product_id``: str - Product - Which product to generate
                  the report for.

            - ``rfq-fills``: dict

                - ``start_date``: str - Start date for items to be included in
                  report.

                - ``end_date``: str - End date for items to be included in
                  report.

                - ``product_id``: str - Product - Which product to generate
                  the report for.

        :param kwargs: Additional keyword arguments.
        """
        return self._post(json=kwargs)

    def get_report(self, report_id: str) -> Dict:
        """
        Get a specific report by `report_id`.

        **INFO**
            Once a report request has been accepted for processing, you can
            poll the report resource endpoint at `/reports/{report_id}` for its
            status. When status is ready, the final report is uploaded and
            available at `{file_url}`.

        :param report_id: The report ID number.
        """
        return self._get(report_id)


class Users(AuthEndpoint):
    """`users` endpoint of the Exchange/Pro API."""

    def get_exchange_limits(self, user_id: str) -> Dict:
        """
        Gets exchange limits information for a single user.

        **INFO**
            This request returns information on your payment method transfer
            limits, as well as buy/sell limits per currency.

        :param user_id: The user ID.
        """
        return self._get(user_id, "exchange-limits")


class WrappedAssets(Endpoint):
    """`wrapped-assets` endpoint of the Exchange/Pro API."""

    def get_assets(self) -> Dict:
        """Returns a list of all supported wrapped assets details objects."""
        return self._get()

    def get_asset_details(self, wrapped_asset_id: str) -> Dict:
        """
        Returns the circulating and total supply of a wrapped asset, and its
        conversion rate.

        **Testing**
            You can use the sandbox environment to test for `cbETH` by sending
            an HTTP GET request to the following URL:

            `https://api-public.sandbox.exchange.coinbase.com/wrapped-assets/CBETH/`

        **Properties:**

            - **Circulating Supply** The number of wrapped asset units in
              possession of customers. It excludes units pre-minted and held
              in abeyance to quickly serve wrapping customers.

              Circulating supply is the most appropriate input to determine
              the market capitalization of a wrapped asset.

            - **Total supply** The total number of wrapped asset units that
              have been minted and exist on-chain.

            - **Conversion rate** The number of underlying staked units that
              can be exchanged for 1 wrapped asset (e.g., the number of ETH2
              units per 1 cbETH unit).

        **TIP**
            Coinbase recommends that you repeatedly query the API, sleeping 1
            second in between queries, to get conversion rate updates
            (currently updated 1x a day) as soon as possible without exceeding
            the rate limit.

        :param wrapped_asset_id: Wrapped asset ID.
        """
        return self._get(wrapped_asset_id)

    def get_asset_conversion_rate(self, wrapped_asset_id: str):
        """
        Returns the conversion rate of a wrapped asset

        **Testing**
            You can use the sandbox environment to test the `cbETH` conversion
            rate by sending an HTTP GET request to the following URL:

            `https://api-public.sandbox.pro.coinbase.com/wrapped-assets/CBETH/conversion-rate`

        **TIP**
            Coinbase recommends that you repeatedly query the API, sleeping 1
            second in between queries, to get conversion rate updates
            (currently updated 1x a day) as soon as possible without exceeding
            the rate limit.

        :param wrapped_asset_id: Wrapped asset ID.
        """
        return self._get(wrapped_asset_id, "conversion-rate")


__all__ = [
    "Time",
    "Accounts",
    "AddressBook",
    "CoinbaseAccounts",
    "Conversions",
    "Currencies",
    "Deposits",
    "PaymentMethods",
    "Transfers",
    "Withdrawals",
    "Fees",
    "Fills",
    "Orders",
    "Oracle",
    "Products",
    "Profiles",
    "Reports",
    "Users",
    "WrappedAssets",
]
