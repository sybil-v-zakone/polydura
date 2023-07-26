from typing import Tuple

from config import (
    GREENFIELD_TESTNET_TUTORIAL_ABI,
    MAINNET_ALPHA_ABI,
    ZK_BRIDGE_ON_OPBNB_ABI,
    ZK_LIGHT_CLIENT_ABI,
)
from utils import read_from_json

from .bridge import Bridge
from .chain import (
    Chain,
    arbitrum,
    avalanche,
    bsc,
    celo,
    combo,
    core,
    fantom,
    gnosis,
    nova,
    opBNB,
    optimism,
    polygon,
)


class NFT:
    def __init__(
        self,
        name,
        mint_chains: Tuple[Chain],
        chain_to_contract_mapping: dict,
        abi,
        mint_chain: Chain | None,
        bridge_chain: Chain | None,
        bridge: Bridge | None = None,
        lz_bridgeable: bool = False,
    ) -> None:
        self.name = name
        self.mint_chains = mint_chains
        self.chain_to_contract_mapping = chain_to_contract_mapping
        self.abi = abi
        self.mint_from = mint_chain
        self.bridge_to = bridge_chain
        self.bridge = bridge
        self.lz_bridgeable = lz_bridgeable

    def __dict__(self):
        return {
            "name": self.name,
            "mint_chains": self.mint_chains.__dict__(),
            "contract_to_chain_mapping": self.chain_to_contract_mapping,
        }


greenfield_testnet_tutorial_NFT = NFT(
    name="Greenfield Testnet Tutorial NFT",
    mint_chains=(bsc),
    chain_to_contract_mapping={
        "bsc": "0x13D23d867e73aF912Adf5d5bd47915261eFa28F2",
    },
    abi=read_from_json(GREENFIELD_TESTNET_TUTORIAL_ABI),
    mint_chain=bsc,
    bridge_chain=None,
)


mainnet_alpha_NFT = NFT(
    name="Mainnet Alpha NFT",
    mint_chains=(core,),
    chain_to_contract_mapping={
        "core": "0x61DFDbcC65DaF1F60fB1DbE703D84940dA28526c",
    },
    abi=read_from_json(MAINNET_ALPHA_ABI),
    mint_chain=core,
    bridge_chain=polygon,
)


ZK_bridge_on_opBNB_NFT = NFT(
    name="ZK Bridge On OpBNB NFT",
    mint_chains=(
        bsc,
        core,
        polygon,
    ),
    chain_to_contract_mapping={
        "bsc": "0x9c614a8E5a23725214024d2C3633BE30D44806f9",
        "polygon": "0xfeb105763753e9d26DfD4aae1Ed368aa7cC18260",
        "core": "0x0f83DA622E36Ee42cfeB222257E1baF20E16a491",
    },
    abi=read_from_json(ZK_BRIDGE_ON_OPBNB_ABI),
    mint_chain=bsc,
    bridge_chain=opBNB,
)


ZK_light_client_NFT = NFT(
    name="ZK Light Client NFT",
    mint_chains=(
        bsc,
        polygon,
    ),
    chain_to_contract_mapping={
        "bsc": "0xD2cCC9EE7Ea2ccd154c727A46D475ddA49E99852",
        "polygon": "0x6b0C248679F493481411a0A14cd5FC2DBBe8Ab02",
    },
    abi=read_from_json(ZK_LIGHT_CLIENT_ABI),
    mint_chain=bsc,
    bridge_chain=opBNB,
)

nfts_list = [
    greenfield_testnet_tutorial_NFT,
    mainnet_alpha_NFT,
    ZK_light_client_NFT,
    ZK_bridge_on_opBNB_NFT,
]
