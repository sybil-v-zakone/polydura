import os
import sys
from pathlib import Path

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent.absolute()
else:
    ROOT_DIR = Path(__file__).parent.parent.absolute()

ABI_DIR = os.path.join(ROOT_DIR, "abi")

GREENFIELD_TESTNET_TUTORIAL_ABI = os.path.join(
    ABI_DIR, "GreenfieldTestnetTutorial_abi.json"
)

rpcs = {
    "bsc": "https://rpc.ankr.com/bsc",
    "polygon": "https://polygon.llamarpc.com",
    "core": "https://rpc.coredao.org",
    "opbnb": "https://opbnb-testnet-rpc.bnbchain.org",
}

chains = ["bsc", "polygon", "core", "opbnb"]

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
