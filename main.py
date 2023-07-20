from loguru import logger

from config import bsc
from models.zk_bridge_client import ZKBridgeClient
from utils import load_keys


def main():
    keys = load_keys()

    for private_key in keys:
        test_client = ZKBridgeClient(
            private_key=private_key,
            network=bsc,
        )

        test_client.load_profile()


if __name__ == "__main__":
    main()
