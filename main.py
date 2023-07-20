from loguru import logger

from models.zk_bridge_client import ZKBridgeClient
from utils import load_keys


def main():
    keys = load_keys()

    for key in keys:
        test_client = ZKBridgeClient(
            key,
            to_chain="polygon",
            from_chain=None,
            network="bsc",
        )

        test_client.load_profile()


if __name__ == "__main__":
    main()
