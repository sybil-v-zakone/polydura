from typing import Optional

from loguru import logger
from web3 import Web3
from web3.middleware import geth_poa_middleware

from .network import Network


class BaseClient:
    def __init__(
        self,
        private_key: str,
        network: Network,
    ) -> None:
        self.private_key = private_key
        self.network = network
        self.w3 = Web3(Web3.HTTPProvider(endpoint_uri=self.network.rpc))
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
        gas_coefficient=1.0,
        value=None,
        max_priority_fee_per_gas: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
    ):
        if not from_:
            from_ = self.address

        tx_params = {
            "chainId": self.w3.eth.chain_id,
            "nonce": self.w3.eth.get_transaction_count(self.address),
            "from": Web3.to_checksum_address(from_),
            "to": Web3.to_checksum_address(to),
        }
        if data:
            tx_params["data"] = data

        if self.network.eip1559_tx:
            w3 = Web3(
                provider=Web3.HTTPProvider(endpoint_uri=self.network.rpc)
            )
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)

            last_block = w3.eth.get_block("latest")
            if not max_priority_fee_per_gas:
                max_priority_fee_per_gas = (
                    BaseClient.get_max_priority_fee_per_gas(
                        w3=w3, block=last_block
                    )
                )
            if not max_fee_per_gas:
                base_fee = int(last_block["baseFeePerGas"] * gas_coefficient)
                max_fee_per_gas = base_fee + max_priority_fee_per_gas

            tx_params["maxPriorityFeePerGas"] = max_priority_fee_per_gas
            tx_params["maxFeePerGas"] = max_fee_per_gas

        else:
            tx_params["gasPrice"] = self.w3.eth.gas_price

        if value:
            tx_params["value"] = value

        try:
            tx_params["gas"] = int(
                self.w3.eth.estimate_gas(tx_params) * gas_coefficient
            )
        except Exception as e:
            logger.exception("Tx failed")
            return None

        sign = self.w3.eth.account.sign_transaction(
            tx_params, self.private_key
        )
        return self.w3.eth.send_raw_transaction(sign.rawTransaction)

    def verify_tx(self, tx_hash) -> bool:
        try:
            data = self.w3.eth.wait_for_transaction_receipt(
                tx_hash, timeout=200
            )
            if "status" in data and data["status"] == 1:
                logger.success(
                    f"{self.address} | transaction was successful: {tx_hash.hex()}"
                )
                return True
            else:
                logger.error(
                    f'{self.address} | transaction failed {data["transactionHash"].hex()}'
                )
                return False
        except Exception as err:
            logger.exception(f"{self.address} | unexpected error: {err}")
            return False
