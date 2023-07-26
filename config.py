import os
import sys
from pathlib import Path

from models.chain import (
    arbitrum,
    avalanche,
    bsc,
    celo,
    combo,
    core,
    fantom,
    gnosis,
    metis,
    moonbeam,
    nova,
    opBNB,
    optimism,
    polygon,
)

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

PRIVATE_KEYS_PATH = "data/private_keys.txt"

DATABASE_PATH = "data/database.json"

PROXIES_PATH = "data/proxies.txt"

ABI_DIR = os.path.join(ROOT_DIR, "abi")

MORALIS_API_KEY = ""

SLEEP_TIME = [300, 500]

MAX_ATTEMPTS = 5

USE_PROXY = True

TG_TOKEN = ""

TG_IDS = []

BITCH_MODE = True

TOKENS_RANGE = 9000

GAS_MULTIPLIER = 1.1

GREENFIELD_TESTNET_TUTORIAL_ABI = os.path.join(
    ABI_DIR, "GreenfieldTestnetTutorial_abi.json"
)

# NFTs ABIs

MAINNET_ALPHA_ABI = os.path.join(ABI_DIR, "MainnetAlpha_abi.json")

ZK_LIGHT_CLIENT_ABI = os.path.join(ABI_DIR, "ZKLightClient_abi.json")

ZK_BRIDGE_ON_OPBNB_ABI = os.path.join(ABI_DIR, "ZKBridgeOnOpBNB_abi.json")

# Bridges ABIs

ZK_BRIDGE_ABI = os.path.join(ABI_DIR, "ZKBridge_abi.json")

LZ_BRIDGE_ABI = os.path.join(ABI_DIR, "LZBridge_abi.json")

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
