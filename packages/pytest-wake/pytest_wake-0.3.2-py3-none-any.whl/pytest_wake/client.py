#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   client.py
@Time    :   2023/02/17 14:15:57
@Version :   1.0
@Desc    :
"""
import json

from requests import Response
from requests import request as _request

from .exception import UnImplementedMethodError, UnSupportVersionError
from .signature import SignatureImpl


class HttpClient:
    def __init__(self, api_key: str = None, api_secret: str = None, recv_window: int = 50000) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.recv_window = recv_window

        if api_key and api_secret:
            self.signimpl = SignatureImpl(self.api_key, self.api_secret, self.recv_window)

    def request(self, method: str, url: str, params_or_body: dict = None, **kwargs) -> Response:
        method = method.lower()
        if method not in ("get", "post"):
            raise UnImplementedMethodError(f"Unimplemented request method: {method}")

        print(f"method: {method}, url: {url}, params_or_body: {params_or_body}")

        need_auth = HttpClient.need_auth(url)

        if "/v2" in url:
            headers = {"Content-Type": "application/json"}
            if method == "get":
                if "private" in url:
                    params_or_body["api_key"] = self.api_key
                    params_or_body["timestamp"] = self.signimpl.now_timestamp
                    params_or_body["recv_window"] = self.recv_window
                    params_or_body["sign"] = self.signimpl.generate(method, url, params_or_body)
                return _request(method, url, params=params_or_body, headers=headers, **kwargs)
            else:
                params_or_body["api_key"] = self.api_key
                params_or_body["timestamp"] = self.signimpl.now_timestamp
                params_or_body["recv_window"] = self.recv_window
                params_or_body["sign"] = self.signimpl.generate(url, params_or_body)
                return _request(method, url, data=json.dumps(params_or_body), headers=headers, **kwargs)

        elif "/v3" in url:
            if method == "get":
                if "private" in url:
                    sign = self.signimpl.generate(method, url, params_or_body)
                    headers = self.signimpl.get_auth_headers(sign)
            else:
                sign = self.signimpl.generate(method, url, params_or_body)
                headers = self.signimpl.get_auth_headers(sign)
            return _request(method, url, data=json.dumps(params_or_body), headers=headers, **kwargs)

        elif "/v5" in url:
            if method == "get":
                if need_auth:
                    sign = self.signimpl.generate(method, url, params_or_body)
                else:
                    sign = None
                headers = self.signimpl.get_auth_headers(sign)
                print(f"headers: {headers}")
                return _request(method, url, params=params_or_body, headers=headers, **kwargs)
            else:
                sign = self.signimpl.generate(method, url, params_or_body)
                headers = self.signimpl.get_auth_headers(sign)
                print(f"headers: {headers}")
                return _request(method, url, data=json.dumps(params_or_body), headers=headers, **kwargs)
        else:
            raise UnSupportVersionError(f"Unrecognized request url: {url}")

    @staticmethod
    def need_auth(url) -> bool:
        flag = False
        if "/v5/" in url:
            # exclude path like `/orderbook/`
            if "/position/" in url or "/order/" in url or "/execution/" in url:
                flag = True
        elif "private" in url:
            flag = True

        return flag
