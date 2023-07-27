from typing import Optional

import requests
from fake_useragent import UserAgent
from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware

from config import GAS_MULTIPLIER
from exceptions.exceptions import GasEstimationError

from .chain import Chain


class BaseClient:
    def __init__(
        self,
        private_key: str,
        chain: Chain,
        proxy,
    ) -> None:
        self.private_key = private_key
        self.chain = chain
        self.proxy = proxy
        self.user_agent = UserAgent().random
        self.session = self.create_session()
        self.w3 = Web3(
            Web3.HTTPProvider(
                endpoint_uri=self.chain.rpc, session=self.session
            )
        )
        self.public_key = Web3.to_checksum_address(
            self.w3.eth.account.from_key(private_key).address
        )

    @staticmethod
    def get_max_priority_fee_per_gas(w3: Web3, block: dict) -> int:
        block_number = block["number"]
        latest_block_transaction_count = w3.eth.get_block_transaction_count(
            block_number
        )
        max_priority_fee_per_gas_list = []
        for i in range(latest_block_transaction_count):
            try:
                transaction = w3.eth.get_transaction_by_block(block_number, i)
                if "maxPriorityFeePerGas" in transaction:
                    max_priority_fee_per_gas_list.append(
                        transaction["maxPriorityFeePerGas"]
                    )
            except Exception as e:
                continue

        if not max_priority_fee_per_gas_list:
            max_priority_fee_per_gas = w3.eth.max_priority_fee
        else:
            max_priority_fee_per_gas_list.sort()
            max_priority_fee_per_gas = max_priority_fee_per_gas_list[
                len(max_priority_fee_per_gas_list) // 2
            ]
        return max_priority_fee_per_gas

    def send_tx(
        self,
        to,
        data=None,
        from_=None,
        gas_multiplier=GAS_MULTIPLIER,
        value=None,
        max_priority_fee_per_gas: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
    ):
        if not from_:
            from_ = self.public_key

        tx_params = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.public_key),
            "from": Web3.to_checksum_address(from_),
            "to": Web3.to_checksum_address(to),
        }
        if data:
            tx_params["data"] = data

        if self.chain.eip1559_tx:
            w3 = Web3(provider=Web3.HTTPProvider(endpoint_uri=self.chain.rpc))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            last_block = w3.eth.get_block("latest")
            if not max_priority_fee_per_gas:
                max_priority_fee_per_gas = (
                    BaseClient.get_max_priority_fee_per_gas(
                        w3=w3, block=last_block
                    )
                )
            if not max_fee_per_gas:
                base_fee = int(last_block["baseFeePerGas"] * gas_multiplier)
                max_fee_per_gas = base_fee + max_priority_fee_per_gas

            tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
            tx_params["maxFeePerGas"] = max_fee_per_gas

        else:
            if self.chain.chain_id == 56:
                tx_params["gasPrice"] = Web3.to_wei(1, "gwei")
            else:
                tx_params["gasPrice"] = self.w3.eth.gas_price

        if value:
            tx_params["value"] = value

        try:
            gas_estimate = self.w3.eth.estimate_gas(tx_params)
            logger.info(f"Gas estimate: {gas_estimate}")
            tx_params["gas"] = int(gas_estimate * gas_multiplier)
        except GasEstimationError:
            logger("Gas required exceeds allowance")
        except Exception as e:
            logger.exception(f"Error estimating gas: {e}")

        try:
            sign = self.w3.eth.account.sign_transaction(
                tx_params, self.private_key
            )
            hash = self.w3.eth.send_raw_transaction(sign.rawTransaction)
        except Exception as e:
            logger.exception(f"Error sending transaction: {e}")
            return None

    def verify_tx(self, tx_hash) -> bool:
        try:
            data = self.w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=200
            )
            if data is None:
                logger.warning(
                    f"{self.public_key} | transaction receipt not available yet."
                )
                return False

            if "status" in data and data["status"] == 1:
                logger.success(
                    f"{self.public_key} | transaction was successful: {tx_hash.hex()}"
                )
                return True
            else:
                logger.error(
                    f'{self.public_key} | transaction failed {data["transactionHash"].hex()}'
                )
                return False
        except Exception as err:
            logger.exception(f"{self.public_key} | unexpected error: {err}")
            return False

    def create_session(self) -> requests.Session:
        session = requests.Session()
        if self.proxy:
            session.proxies = {
                "http": f"http://{self.proxy}",
                "https": f"http://{self.proxy}",
            }
        return session
