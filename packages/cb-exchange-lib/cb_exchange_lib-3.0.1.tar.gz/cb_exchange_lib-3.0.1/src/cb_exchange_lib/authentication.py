# -*- coding: UTF-8 -*-

from abc import ABC
from base64 import b64encode, b64decode
from hashlib import sha256
from hmac import HMAC
from typing import Union

from requests.auth import AuthBase
from requests.models import PreparedRequest
from requests.utils import to_native_string

from .utils import encode, decode, get_posix


class HMACBase(ABC):
    """Requests signing handler."""

    @staticmethod
    def _pre_hash(timestamp: float, method: str, path: str, body: str = None) -> bytes:
        """
        Create the pre-hash string by concatenating the timestamp with
        the request method, path and body if not None.
        """
        if body is not None:
            return encode(f"{timestamp}{method.upper()}{path}{decode(body)}")
        return encode(f"{timestamp}{method.upper()}{path}")

    @staticmethod
    def _sign(key: bytes, message: bytes) -> bytes:
        """
        Create a sha256 HMAC and sign the required `message` using the
        API base64 decoded secret as `key`.
        """
        hmac = HMAC(key=key, msg=message, digestmod=sha256)
        return b64encode(hmac.digest())

    @staticmethod
    def _headers(key: str, signature: bytes, timestamp: float, passphrase: str) -> dict:
        return {
            "CB-ACCESS-KEY": to_native_string(key),
            "CB-ACCESS-SIGN": to_native_string(signature),
            "CB-ACCESS-TIMESTAMP": to_native_string(str(timestamp)),
            "CB-ACCESS-PASSPHRASE": to_native_string(passphrase),
        }

    def __init__(self, key: str, passphrase: str, secret: str):
        """
        :param key: The API key;
        :param passphrase: The API passphrase;
        :param secret: The API secret;
        """
        self.__key = key
        self.__passphrase = passphrase
        self.__secret = b64decode(encode(secret))

    def _get_signature(self, method: str, path: str, body: Union[bytes, str] = None) -> dict:
        timestamp = get_posix()
        message = self._pre_hash(
            timestamp=timestamp,
            method=method.upper(),
            path=path,
            body=body
        )
        return self._headers(
            key=self.__key,
            signature=self._sign(self.__secret, message),
            timestamp=timestamp,
            passphrase=self.__passphrase,
        )


class WSAuth(HMACBase):
    """Websocket client HMAC authentication handler."""

    @staticmethod
    def _headers(key: str, signature: bytes, timestamp: float, passphrase: str) -> dict:
        return {
            "key": to_native_string(key),
            "signature": to_native_string(signature),
            "timestamp": to_native_string(str(timestamp)),
            "passphrase": to_native_string(passphrase),
        }

    def sign(self, method: str, path: str, params: dict):
        signature = self._get_signature(method=method, path=path)
        params.update(signature)


class SessionAuth(AuthBase, HMACBase):
    """Session HMAC authentication handler."""

    def __call__(self, request: PreparedRequest):
        self.sign(request)
        return request

    def sign(self, request: PreparedRequest):
        signature = self._get_signature(
            method=request.method,
            path=request.path_url,
            body=request.body
        )
        request.headers.update(signature)


__all__ = ["SessionAuth", "WSAuth"]
