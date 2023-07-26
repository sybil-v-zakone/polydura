import random

import requests
from eth_account.messages import encode_defunct
from loguru import logger
from web3 import Web3

from config import (
    BITCH_MODE,
    GAS_MULTIPLIER,
    MAX_ATTEMPTS,
    TOKENS_RANGE,
    headers,
)
from models.bridge import Bridge, lz_bridge, zk_bridge
from models.chain import Chain, destination_chains, source_chains

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
    ) -> None:
        super().__init__(private_key, chain, proxy)
        self.nfts_to_mint = [
            ZK_bridge_on_opBNB_NFT.name,
            mainnet_alpha_NFT.name,
            ZK_light_client_NFT.name,
            greenfield_testnet_tutorial_NFT.name,
        ]
        self.minted_nfts = []
        self.bridged_nfts = []
        self.message_sent = False

    def to_dict(self):
        return {
            "private_key": self.private_key,
            "public_key": self.public_key,
            "proxy": self.proxy,
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

                logger.success("Signature recieved")

                return signature

        except Exception as e:
            logger.exception(f"Get signature exception: {e}")

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
            response = self.session.get(url=url, headers=cookie)
            if response.status_code == 200:
                logger.success("Successfully loaded the profile")
                return True

        except Exception as e:
            logger.exception(f"Profile load error: {e}")

    def mint_random_nft(self, max_attempts=MAX_ATTEMPTS):
        nft_name = random.choice(self.nfts_to_mint)

        logger.info(f"Chose to mint {nft_name}.")

        nft = next((nft for nft in nfts_list if nft.name == nft_name), None)

        logger.info("Checking if client's chain is available for minting.")

        if self.chain in nft.mint_chains:
            logger.info("Chain is available.")
        else:
            logger.info(
                f"Chain unavailable. Changing chain to {nft.mint_from}."
            )

            self.change_chain(nft.mint_from)

        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(
                nft.chain_to_contract_mapping[f"{self.chain}"]
            ),
            abi=nft.abi,
        )

        logger.info(f"Contract initialized.")
        logger.info(f"Checking amount of minted NFTs.")

        allowed_to_mint = contract.functions.getMintSurplus(
            self.public_key
        ).call()

        data = contract.encodeABI("mint")

        for attempt in range(max_attempts):
            if allowed_to_mint > 0:
                logger.info("Sending a mint tx.")
                tx_hash = self.send_tx(
                    to=nft.chain_to_contract_mapping[f"{self.chain}"],
                    data=data,
                    gas_multiplier=GAS_MULTIPLIER,
                )

                logger.info(
                    f"Sent a mint tx with a hash: {Web3.to_hex(tx_hash)}"
                )

                logger.info("Verifying tx...")

                if self.verify_tx(tx_hash=tx_hash):
                    self.nfts_to_mint.remove(f"{nft_name}")
                    self.minted_nfts.append(f"{nft_name}")
                    return nft
                else:
                    logger.error("Transaction verification failed.")
            else:
                logger.error("Mint limit exceeded.")

        logger.error("Max attempts reached without success.")
        return None

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
                f"Sent an approve tx with a hash: {Web3.to_hex(tx_hash)}"
            )
            logger.info("Verifying tx...")

            if self.verify_tx(tx_hash=tx_hash):
                return True
            else:
                return False

        except Exception as e:
            logger.info(
                f"Error occurred while approving {nft.name} for {bridge.name}."
            )

    def bridge_nft(self, nft: NFT):
        if BITCH_MODE:
            destination_chain = nft.bridge_to
        else:
            destination_chain = random.choice(destination_chains)

        if self.chain.supports_lz and destination_chain.supports_lz:
            bridge = lz_bridge
        else:
            bridge = zk_bridge

        logger.info(f"Chosen bridge: {bridge.name}")
        logger.info(f"Current client's chain: {self.chain}")

        contract_address = bridge.chain_to_contract_mapping[self.chain.name]

        logger.info(f"Contract address for bridging: {contract_address}")

        token_id = self.get_token_id(nft=nft)

    def get_token_id(self, nft: NFT):
        contract = self.w3.eth.contract(
            address=nft.chain_to_contract_mapping[f"{self.chain.name}"],
            abi=nft.abi,
        )

        logger.info("Checking contract's total supply.")
        try:
            last_token_id = contract.functions.totalSupply().call()
            logger.success(f"Total supply is {last_token_id}.")
        except Exception as e:
            logger.error(f"Couldn't retrieve contract's total supply: {e}.")

        logger.info(
            f"Checking token ID of {nft.name} for owner {self.public_key}"
        )
        try:
            # start < stop
            token_id = contract.functions.tokensOfOwnerIn(
                self.public_key,  # start
                last_token_id - TOKENS_RANGE,  # stop
                last_token_id,
            ).call()

            if token_id:
                logger.success(f"Token ID is {token_id[0]}.")
                return token_id[0]
            else:
                logger.error(
                    f"Range is too short for token {nft.name} at {self.public_key}"
                )

        except Exception as e:
            logger.exception(f"Couldn't retrieve owned token ID: {e}")

    def change_chain(self, chain):
        self.chain = chain
        self.w3 = Web3(
            Web3.HTTPProvider(endpoint_uri=chain.rpc, session=self.session)
        )

    def get_ip():
        response = requests.get("https://api64.ipify.org?format=json").json()
        return response["ip"]
