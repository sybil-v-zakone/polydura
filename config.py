import os
import sys
from pathlib import Path

from models.network import Network
from models.NFT import NFT
from utils import load_json_file

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

ABI_DIR = os.path.join(ROOT_DIR, "abi")

GREENFIELD_TESTNET_TUTORIAL_ABI = os.path.join(
    ABI_DIR, "GreenfieldTestnetTutorial_abi.json"
)

MAINNET_ALPHA_ABI = os.path.join(ABI_DIR, "MainnetAlpha_abi.json")

ZK_LIGHT_CLIENT_ABI = os.path.join(ABI_DIR, "ZKLightClient_abi.json")

ZK_BRIDGE_ON_OPBNB_ABI = os.path.join(ABI_DIR, "ZKBridgeOnOpBNB_abi.json")

rpcs = {
    "bsc": "https://rpc.ankr.com/bsc",
    "polygon": "https://polygon.llamarpc.com",
    "core": "https://rpc.coredao.org",
    "opbnb": "https://opbnb-testnet-rpc.bnbchain.org",
}

headers = {
    "authority": "api.zkbridge.com",
    "method": "OPTIONS",
    "path": "/api/signin/validation_message",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "access-control-request-headers": "content-type",
    "access-control-request-method": "POST",
    "origin": "https://zkbridge.com",
    "referer": "https://zkbridge.com/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
}

# List of available networks

polygon = Network(
    name="polygon",
    rpc="https://polygon-rpc.com/",
    chain_id=137,
    eip1559_tx=True,
    coin_symbol="MATIC",
    explorer="https://polygonscan.com/",
)


bsc = Network(
    name="bsc",
    rpc="https://rpc.ankr.com/bsc",
    chain_id=56,
    eip1559_tx=True,
    coin_symbol="BNB",
    explorer="https://bscscan.com/",
)


core = Network(
    name="core",
    rpc="https://rpc.coredao.org",
    chain_id=1116,
    eip1559_tx=True,
    coin_symbol="CORE",
    explorer="https://scan.coredao.org/",
)


celo = Network(
    name="celo",
    rpc="https://rpc.ankr.com/celo",
    chain_id=42220,
    eip1559_tx=True,
    coin_symbol="CELO",
    explorer="https://celoscan.io/",
)


arbitrum = Network(
    name="arbitrum",
    rpc="https://rpc.ankr.com/arbitrum/",
    chain_id=42161,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://arbiscan.io/",
)


optimism = Network(
    name="optimism",
    rpc="https://rpc.ankr.com/optimism/",
    chain_id=10,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://optimistic.etherscan.io/",
)


avalanche = Network(
    name="avalanche",
    rpc="https://rpc.ankr.com/avalanche/",
    chain_id=43114,
    eip1559_tx=True,
    coin_symbol="AVAX",
    explorer="https://snowtrace.io/",
)


fantom = Network(
    name="fantom",
    rpc="https://rpc.ankr.com/fantom/",
    chain_id=250,
    eip1559_tx=True,
    coin_symbol="FTM",
    explorer="https://ftmscan.com/",
)


opBNB = Network(
    name="opBNB",
    rpc="https://opbnb-testnet-rpc.bnbchain.org",
    chain_id=5611,
    eip1559_tx=True,
    coin_symbol="tBNB",
    explorer="https://opbnbscan.com/",
)


combo = Network(
    name="combo",
    rpc="https://test-rpc.combonetwork.io",
    chain_id=91715,
    eip1559_tx=True,
    coin_symbol="tcBNB",
    explorer="https://combotrace-testnet.nodereal.io/",
)


nova = Network(
    name="nova",
    rpc="https://nova.arbitrum.io/rpc",
    chain_id=42170,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://nova.arbiscan.io/",
)


moonbeam = Network(
    name="moonbeam",
    rpc="https://rpc.ankr.com/moonbeam",
    chain_id=1284,
    eip1559_tx=True,
    coin_symbol="GLMR",
    explorer="https://moonscan.io/",
)


gnosis = Network(
    name="gnosis",
    rpc="https://rpc.ankr.com/gnosis",
    chain_id=100,
    eip1559_tx=True,
    coin_symbol="XDAI",
    explorer="https://gnosisscan.io/",
)


metis = Network(
    name="metis",
    rpc="https://andromeda.metis.io/?owner=1088",
    chain_id=1088,
    eip1559_tx=True,
    coin_symbol="METIS",
    explorer="https://andromeda-explorer.metis.io/",
)

chains = [
    polygon,
    bsc,
    core,
    celo,
    arbitrum,
    avalanche,
    fantom,
    opBNB,
    optimism,
    metis,
    gnosis,
    moonbeam,
    nova,
    combo,
]

# List of avalable NFTs

greenfield_testnet_tutorial_NFT = NFT(
    name="Greenfield Testnet Tutorial NFT",
    mint_chains=(bsc),
    contract_chain_mapping={
        "bsc": "0x13D23d867e73aF912Adf5d5bd47915261eFa28F2",
    },
    abi=load_json_file(GREENFIELD_TESTNET_TUTORIAL_ABI),
)


mainnet_alpha_NFT = NFT(
    name="Mainnet Alpha NFT",
    mint_chains=(
        bsc,
        core,
        polygon,
    ),
    contract_chain_mapping={
        "bsc": "0xC5ae0d15593316e0cC905840eD2dE83E2DD4EA9E",
        "polygon": "0x9d5d479a84f3358e8e27afe056494bd2da239acd",
        "core": "0x61DFDbcC65DaF1F60fB1DbE703D84940dA28526c",
    },
    abi=load_json_file(MAINNET_ALPHA_ABI),
)


ZK_bridge_on_opBNB_NFT = NFT(
    name="ZK Bridge On OpBNB NFT",
    mint_chains=(
        bsc,
        core,
        polygon,
    ),
    contract_chain_mapping={
        "bsc": "0x9c614a8E5a23725214024d2C3633BE30D44806f9",
        "polygon": "0xfeb105763753e9d26DfD4aae1Ed368aa7cC18260",
        "core": "0x0f83DA622E36Ee42cfeB222257E1baF20E16a491",
    },
    abi=load_json_file(ZK_BRIDGE_ON_OPBNB_ABI),
)


ZK_light_client_NFT = NFT(
    name="ZK Light Client NFT",
    mint_chains=(
        bsc,
        polygon,
    ),
    contract_chain_mapping={
        "bsc": "0xD2cCC9EE7Ea2ccd154c727A46D475ddA49E99852",
        "polygon": "0x6b0C248679F493481411a0A14cd5FC2DBBe8Ab02",
    },
    abi=load_json_file(ZK_LIGHT_CLIENT_ABI),
)
