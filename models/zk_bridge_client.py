import random

import requests
from eth_abi.packed import encode_packed
from eth_account.messages import encode_defunct
from loguru import logger
from web3 import Web3

from config import (
    BITCH_MODE,
    GAS_MULTIPLIER,
    MAX_ATTEMPTS,
    TOKENS_RANGE,
    WEB_SLEEP_TIME,
    headers,
)
from models.bridge import Bridge, lz_bridge, zk_bridge
from models.chain import Chain, destination_chains, source_chains
from utils import sleep

from .base_client import BaseClient
from .NFT import (
    NFT,
    ZK_bridge_on_opBNB_NFT,
    ZK_light_client_NFT,
    greenfield_testnet_tutorial_NFT,
    mainnet_alpha_NFT,
    nfts_list,
)


class ZKBridgeClient(BaseClient):
    def __init__(
        self,
        private_key: str,
        chain: Chain,
        proxy,
        minted_nfts=[],
        bridged_nfts=[],
        message_sent=False,
        nfts_to_mint=[
            ZK_bridge_on_opBNB_NFT.name,
            mainnet_alpha_NFT.name,
            ZK_light_client_NFT.name,
            greenfield_testnet_tutorial_NFT.name,
        ],
    ) -> None:
        super().__init__(private_key, chain, proxy)
        self.nfts_to_mint = nfts_to_mint
        self.minted_nfts = minted_nfts
        self.bridged_nfts = bridged_nfts
        self.message_sent = message_sent

    def to_dict(self):
        return {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "proxy": self.proxy,
            "chain": self.chain.name,
            "nfts_to_mint": self.nfts_to_mint,
            "minted_nfts": self.minted_nfts,
            "bridged_nfts": self.bridged_nfts,
            "message_sent": self.message_sent,
        }

    def get_signature(self):
        url = "https://api.zkbridge.com/api/signin/validation_message"
        user_agent = self.user_agent

        request_headers = headers.copy()
        request_headers["user-agent"] = user_agent

        json = {"publicKey": self.public_key.lower()}

        try:
            self.session.request("OPTIONS", url=url, headers=request_headers)
            response = self.session.post(
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

                logger.success(f"{self.public_key} | Signature recieved")

                return signature

        except Exception as e:
            logger.exception(
                f"{self.public_key} | Exception occurred when generating a signature: {e}"
            )

    @sleep(secs=random.randint(WEB_SLEEP_TIME[0], WEB_SLEEP_TIME[1]))
    def get_cookie(self):
        signature = self.get_signature()

        request_headers = headers.copy()
        request_headers["user-agent"] = self.user_agent

        url = "https://api.zkbridge.com/api/signin"

        json = {
            "publicKey": self.public_key.lower(),
            "signedMessage": signature,
        }

        try:
            self.session.request("OPTIONS", url=url, headers=request_headers)
            response = self.session.post(
                url=url,
                headers=request_headers,
                json=json,
            )

            if response.status_code == 200:
                token = response.json()["token"]
                request_headers["authorization"] = f"Bearer {token}"

                logger.success(f"{self.public_key} | Cookie recieved")

                return request_headers

        except Exception as e:
            logger.exception(
                f"{self.public_key} | Did not recieve the cookie: {e}"
            )

    @sleep(secs=random.randint(WEB_SLEEP_TIME[0], WEB_SLEEP_TIME[1]))
    def load_profile(self):
        cookie = self.get_cookie()

        url = "https://api.zkbridge.com/api/user/profile?"

        try:
            response = self.session.get(url=url, headers=cookie)
            if response.status_code == 200:
                logger.success(
                    f"{self.public_key} | Successfully loaded the profile"
                )
                return True

        except Exception as e:
            logger.exception(f"{self.public_key} | Profile load error: {e}")

    @sleep()
    def mint_random_nft(self, max_attempts=MAX_ATTEMPTS):
        try:
            nft_name: str = random.choice(self.nfts_to_mint)
            logger.info(f"{self.public_key} | NFT name: {nft_name}.")
        except IndexError:
            logger.success(f"{self.public_key} | All nfts were minted.")
        except Exception as e:
            logger.exception(
                f"{self.public_key} | Unexpected error when minting: {e}"
            )

        logger.info(f"{self.public_key} | Chose to mint {nft_name}.")

        nft = next((nft for nft in nfts_list if nft.name == nft_name), None)

        if BITCH_MODE:
            if self.chain != nft.cheapest_mint_chain:
                logger.info(
                    f"{self.public_key} | Changing chain to {nft.cheapest_mint_chain}."
                )
                self.change_chain(nft.cheapest_mint_chain)

        logger.info(
            f"{self.public_key} | Checking if client's chain is available for minting."
        )

        if self.chain in nft.mint_chains:
            logger.info(f"{self.public_key} | Chain is available.")
        else:
            logger.info(
                f"{self.public_key} | Chain unavailable. Changing chain to {nft.cheapest_mint_chain}."
            )
            self.change_chain(random.choice(source_chains))

        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(
                nft.chain_to_contract_mapping[f"{self.chain}"]
            ),
            abi=nft.abi,
        )

        logger.info(f"{self.public_key} | Contract initialized.")
        logger.info(f"{self.public_key} | Checking amount of minted NFTs.")

        allowed_to_mint = contract.functions.getMintSurplus(
            self.public_key
        ).call()

        data = contract.encodeABI("mint")

        if allowed_to_mint > 0:
            for attempt in range(max_attempts):
                logger.info(f"{self.public_key} | Sending a mint tx.")
                tx_hash = self.send_tx(
                    to=nft.chain_to_contract_mapping[f"{self.chain}"],
                    data=data,
                )
                logger.info(
                    f"{self.public_key} | Sent a mint tx with a hash: {Web3.to_hex(tx_hash)}"
                )
                logger.info(f"{self.public_key} | Verifying tx.")
                if self.verify_tx(tx_hash=tx_hash):
                    self.nfts_to_mint.remove(nft_name)
                    self.minted_nfts.append(nft_name)
                    return nft
                else:
                    logger.error(
                        f"{self.public_key} | Transaction verification failed."
                    )
        else:
            logger.error(
                f"{self.public_key} | Mint limit for {nft.name} exceeded."
            )
            self.nfts_to_mint.remove(nft_name)
            self.minted_nfts.append(nft_name)

            return None

        logger.error(
            f"{self.public_key} | Max attempts reached without success."
        )
        return False

    @sleep()
    def approve_nft(self, bridge: Bridge, nft: NFT):
        nft_contract_address = nft.chain_to_contract_mapping[f"{self.chain}"]

        contract = self.w3.eth.contract(
            address=nft_contract_address,
            abi=nft.abi,
        )

        token_id = self.get_token_id(nft=nft)
        to = bridge.chain_to_contract_mapping[f"{self.chain}"]
        data = contract.encodeABI("approve", args=(to, token_id))

        try:
            tx_hash = self.send_tx(
                to=nft_contract_address,
                data=data,
                gas_multiplier=GAS_MULTIPLIER,
            )

            logger.info(
                f"{self.public_key} | Sent an approve tx with a hash: {Web3.to_hex(tx_hash)}"
            )
            logger.info(f"{self.public_key} | Verifying tx.")

            if self.verify_tx(tx_hash=tx_hash):
                return token_id
            else:
                return None

        except Exception as e:
            logger.info(
                f"{self.public_key} | Error occurred while approving {nft.name} for {bridge.name}."
            )

    @sleep()
    def bridge_nft(self, nft: NFT):
        if BITCH_MODE:
            destination_chain = nft.cheapest_destination
        else:
            destination_chain = random.choice(destination_chains)

        logger.info(
            f"{self.public_key} | Current client's chain: {self.chain}"
        )
        logger.info(
            f"{self.public_key} | Chosen destination chain: {destination_chain.name}"
        )

        if self.chain.supports_lz and destination_chain.supports_lz:
            token_id = self.approve_nft(bridge=lz_bridge, nft=nft)

            nft = self.lz_nft_bridge(
                nft=nft,
                destination_chain=destination_chain,
                token_id=token_id,
            )
        else:
            token_id = self.approve_nft(bridge=zk_bridge, nft=nft)

            nft = self.zk_nft_bridge(
                nft=nft,
                destination_chain=destination_chain,
                token_id=token_id,
            )

        try:
            self.minted_nfts.remove(nft.name)
            self.bridged_nfts.append(nft.name)
        except Exception as e:
            logger.exception(
                f"{self.public_key} | Unexpected error updating the database for value <{nft.name}>: {e}"
            )

    def lz_nft_bridge(self, nft: NFT, token_id: int, destination_chain: Chain):
        logger.info(f"{self.public_key} | Bridging using {lz_bridge.name}")

        nft_contract_address = nft.chain_to_contract_mapping[
            f"{self.chain.name}"
        ]

        bridge_contract_address = lz_bridge.chain_to_contract_mapping[
            f"{self.chain.name}"
        ]
        bridge_contract = self.w3.eth.contract(
            address=bridge_contract_address,
            abi=lz_bridge.abi,
        )

        adapter_params = self.w3.to_hex(
            encode_packed(["uint16", "uint256"], [1, 200000])
        )

        fee = bridge_contract.functions.estimateFee(
            nft_contract_address,
            token_id,
            destination_chain.lz_chain_id,
            self.public_key,
            adapter_params,
        ).call()

        data = bridge_contract.encodeABI(
            "transferNFT",
            args=(
                nft_contract_address,
                token_id,
                destination_chain.lz_chain_id,
                self.public_key,
                adapter_params,
            ),
        )

        logger.info(f"LayerZero bridge fee is: {fee}")
        logger.info(f"{self.public_key} | Sending LayerZero bridge tx.")
        try:
            tx_hash = self.send_tx(
                to=bridge_contract_address,
                data=data,
                value=fee,
            )

            logger.info(
                f"{self.public_key} | Sent a LayerZero bridge tx with a hash: {Web3.to_hex(tx_hash)}"
            )
            logger.info(f"{self.public_key} | Verifying tx.")

            if self.verify_tx(tx_hash=tx_hash):
                return nft
            else:
                return None

        except Exception as e:
            logger.exception(
                f"{self.public_key} | An error occurred while bridging with LayerZero: {e}"
            )
            return None

    def zk_nft_bridge(self, nft: NFT, token_id: int, destination_chain: Chain):
        logger.info(f"{self.public_key} | Bridging using {zk_bridge.name}")

        if BITCH_MODE:
            destination_chain = nft.cheapest_destination
        else:
            destination_chain = random.choice(destination_chains)

        nft_contract_address = nft.chain_to_contract_mapping[
            f"{self.chain.name}"
        ]

        bridge_contract_address = zk_bridge.chain_to_contract_mapping[
            f"{self.chain.name}"
        ]
        bridge_contract = self.w3.eth.contract(
            address=bridge_contract_address,
            abi=zk_bridge.abi,
        )

        fee = bridge_contract.functions.fee(
            destination_chain.zk_chain_id
        ).call()

        zero_padded_public_address = self.get_zero_padded_address()

        data = bridge_contract.encodeABI(
            "transferNFT",
            args=(
                nft_contract_address,
                token_id,
                destination_chain.zk_chain_id,
                zero_padded_public_address,
            ),
        )

        logger.info(f"ZKbridge bridge fee is: {fee}")
        logger.info(f"{self.public_key} | Sending ZKBridge bridge tx.")

        try:
            tx_hash = self.send_tx(
                bridge_contract_address,
                data=data,
                value=fee,
            )

            logger.info(
                f"{self.public_key} | Sent a ZKBridge bridge tx with a hash: {Web3.to_hex(tx_hash)}"
            )
            logger.info("Verifying tx.")

            if self.verify_tx(tx_hash=tx_hash):
                return nft
            else:
                return None

        except Exception as e:
            logger.exception(
                f"{self.public_key} | An error occurred while bridging with ZKBridge: {e}."
            )
            return None

    def get_token_id(self, nft: NFT):
        contract = self.w3.eth.contract(
            address=nft.chain_to_contract_mapping[f"{self.chain.name}"],
            abi=nft.abi,
        )

        logger.info(f"{self.public_key} | Checking contract's total supply.")
        try:
            last_token_id = contract.functions.totalSupply().call()
            logger.info(
                f"{self.public_key} | Total supply is {last_token_id}."
            )
        except Exception as e:
            logger.error(
                f"{self.public_key} | Couldn't retrieve contract's total supply: {e}."
            )
            return None

        logger.info(f"{self.public_key} | Checking token ID of {nft.name}.")
        try:
            token_id = None
            for token_range_stop in range(last_token_id, -1, -TOKENS_RANGE):
                token_range_start = max(token_range_stop - TOKENS_RANGE + 1, 0)
                try:
                    token_id = contract.functions.tokensOfOwnerIn(
                        self.public_key, token_range_start, token_range_stop
                    ).call()
                    if token_id:
                        logger.info(
                            f"{self.public_key} | Token ID is {token_id[0]}."
                        )
                        return token_id[0]
                except Exception as e:
                    logger.error(
                        f"{self.public_key} | Failed to retrieve token ID in range [{token_range_start}, {token_range_stop}]: {e}."
                    )

            logger.error(
                f"{self.public_key} | Token ID not found for {nft.name}."
            )
            return None

        except Exception as e:
            logger.exception(
                f"{self.public_key} | Couldn't retrieve owned token ID: {e}"
            )
            return None

    def change_chain(self, chain):
        self.chain = chain
        self.w3 = Web3(
            Web3.HTTPProvider(endpoint_uri=chain.rpc, session=self.session)
        )

    def get_zero_padded_address(self):
        return self.w3.to_hex(
            self.w3.to_bytes(hexstr=self.public_key).rjust(32, b"\x00")
        )

    def get_ip(self):
        response = self.session.get(
            "https://api64.ipify.org?format=json"
        ).json()
        return response["ip"]

    @staticmethod
    def client_from_db_item(db_item):
        private_key = db_item.get("private_key")
        chain_name = db_item.get("chain")
        proxy = db_item.get("proxy")
        nfts_to_mint = db_item.get(
            "nfts_to_mint",
            [
                ZK_bridge_on_opBNB_NFT.name,
                mainnet_alpha_NFT.name,
                ZK_light_client_NFT.name,
                greenfield_testnet_tutorial_NFT.name,
            ],
        )
        minted_nfts = db_item.get("minted_nfts", [])
        bridged_nfts = db_item.get("bridged_nfts", [])
        message_sent = db_item.get("message_sent", False)

        chain = next(
            (chain for chain in source_chains if chain.name == chain_name),
            None,
        )

        return ZKBridgeClient(
            private_key=private_key,
            chain=chain,
            proxy=proxy,
            nfts_to_mint=nfts_to_mint,
            minted_nfts=minted_nfts,
            bridged_nfts=bridged_nfts,
            message_sent=message_sent,
        )
