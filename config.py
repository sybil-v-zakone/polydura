import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.absolute()

PRIVATE_KEYS_PATH = "data/private_keys.txt"

DATABASE_PATH = "data/database.json"

PROXIES_PATH = "data/proxies.txt"

ABI_DIR = os.path.join(ROOT_DIR, "abi")

TX_SLEEP_TIME = [200, 500]

REQUEST_SLEEP_TIME = [5, 15]

MAX_ATTEMPTS = 5

USE_PROXY = False  # Use proxy if "True" else "False"

BITCH_MODE = True  # Use cheapest routes if "True", if "False" use random routes

TOKENS_RANGE = 1000  # Range for each step when checking client's NFT token ID

GAS_MULTIPLIER = 1.1

# minimum balance in wei
MIN_CLIENT_BALANCE = 40000000000000

# NFTs ABIs

GREENFIELD_TESTNET_TUTORIAL_ABI = os.path.join(ABI_DIR, "GreenfieldTestnetTutorial_abi.json")

MAINNET_ALPHA_ABI = os.path.join(ABI_DIR, "MainnetAlpha_abi.json")

ZK_LIGHT_CLIENT_ABI = os.path.join(ABI_DIR, "ZKLightClient_abi.json")

ZK_BRIDGE_ON_OPBNB_ABI = os.path.join(ABI_DIR, "ZKBridgeOnOpBNB_abi.json")

PANDRA_CODECONQUEROR_ABI = os.path.join(ABI_DIR, "PandraCodeConqueror_abi.json")

PANDRA_PIXELPROWLER_ABI = os.path.join(ABI_DIR, "PandraPixelProwler_abi.json")

PANDRA_ECOGUARDIAN_ABI = os.path.join(ABI_DIR, "PandraEcoGuardian_abi.json")

PANDRA_MELODY_MAVEN_ABI = os.path.join(ABI_DIR, "PandraMelodyMaven_abi.json")

# Bridges ABIs

ZK_BRIDGE_ABI = os.path.join(ABI_DIR, "ZKBridge_abi.json")

LZ_BRIDGE_ABI = os.path.join(ABI_DIR, "LZBridge_abi.json")

# Mailer ABI

LZ_MAILER_ABI = os.path.join(ABI_DIR, "LzMailer_abi.json")

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

MESSENGER_CONTRACT_ADDRESS = "0xf0295A8caD5f287CC52b6F5994fE4aa6FB6e8D4B"
