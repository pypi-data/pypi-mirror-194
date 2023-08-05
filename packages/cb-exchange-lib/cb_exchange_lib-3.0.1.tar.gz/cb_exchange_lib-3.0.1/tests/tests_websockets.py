# -*- coding: UTF-8 -*-

from dataclasses import dataclass

from keyring import get_password
from websocket import enableTrace

from src.cb_exchange_lib import MarketData, DirectMarketData
from src.cb_exchange_lib.constants import DIRECT_MARKET_DATA

enableTrace(True)

ENVIRONMENT: str = "production"
# ENVIRONMENT: str = "sandbox"


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

    auth = Credentials(DIRECT_MARKET_DATA.get(ENVIRONMENT))

    # ******************** MarketData: ******************** #
    #
    # client = MarketData(
    #     environment=ENVIRONMENT,
    #     debug=True,
    #     channels=["ticker"],
    #     product_ids=["BTC-USD"],
    # )
    # client.listen()
    #
    # try:
    #     for item in client.queue:
    #         print(item)
    # except KeyboardInterrupt:
    #     client.close()

    # ******************** DirectMarketData: ******************** #

    client = DirectMarketData(
        **auth.as_dict(),
        environment=ENVIRONMENT,
        debug=True,
        channels=[
            {
                "name": "ticker",
                "product_ids": [
                    "BTC-USD"
                ]
            }
        ]
    )
    client.listen()

    try:
        for item in client.queue:
            print(item)
    except KeyboardInterrupt:
        client.close()
