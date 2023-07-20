import requests
from eth_account.messages import encode_defunct
from fake_useragent import UserAgent
from loguru import logger
from web3 import Web3

from config import chains, headers, rpcs
from models.network import Network

from .base_client import BaseClient


class ZKBridgeClient(BaseClient):
    def __init__(self, private_key, network: Network) -> None:
        super().__init__(private_key, network)
        self.account = self.w3.eth.account.from_key(private_key)
        self.public_key = self.account.address

    def get_signature(self):
        url = "https://api.zkbridge.com/api/signin/validation_message"
        user_agent = UserAgent().random

        request_headers = headers.copy()
        request_headers["user-agent"] = user_agent

        json = {"publicKey": self.public_key.lower()}

        try:
            requests.request("OPTIONS", url=url, headers=request_headers)
            response = requests.post(
                url=url,
                headers=request_headers,
                json=json,
            )

            if response.status_code == 200:
                message = encode_defunct(text=response.json()["message"])

                signed_message = self.w3.eth.account.sign_message(
                    message, self.private_key
                )

                signature = self.w3.to_hex(signed_message.signature)

                logger.success("Signature recieved")

                return signature, user_agent

        except Exception as e:
            logger.exception(f"Get signature exception: {e}")

    def get_cookie(self):
        signature, user_agent = self.get_signature()

        request_headers = headers.copy()
        request_headers["user-agent"] = user_agent

        url = "https://api.zkbridge.com/api/signin"

        json = {
            "publicKey": self.public_key.lower(),
            "signedMessage": signature,
        }

        try:
            requests.request("OPTIONS", url=url, headers=request_headers)
            response = requests.post(
                url=url,
                headers=request_headers,
                json=json,
            )

            if response.status_code == 200:
                token = response.json()["token"]
                request_headers["authorization"] = f"Bearer {token}"

                logger.success("Cookie recieved")

                return request_headers

        except Exception as e:
            logger.exception(f"Did not recieve the cookie: {e}")

    def load_profile(self):
        cookie = self.get_cookie()

        url = "https://api.zkbridge.com/api/user/profile?"

        try:
            response = requests.get(url=url, headers=cookie)
            if response.status_code == 200:
                logger.success("Successfully loaded the profile")
                return True

        except Exception as e:
            logger.exception(f"Profile load error: {e}")

    def mint():
        pass
