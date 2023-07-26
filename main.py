from config import PRIVATE_KEYS_PATH, PROXIES_PATH
from models.bridge import zk_bridge
from models.chain import bsc, polygon
from models.database import Database
from models.NFT import ZK_bridge_on_opBNB_NFT, ZK_light_client_NFT
from models.zk_bridge_client import ZKBridgeClient
from utils import read_from_txt


def main():
    keys = read_from_txt(PRIVATE_KEYS_PATH)
    proxies = read_from_txt(PROXIES_PATH)

    for private_key, proxy in zip(keys, proxies):
        test_client = ZKBridgeClient(
            private_key=private_key,
            chain=bsc,
            proxy=proxy,
        )

        # test_client.load_profile()
        # test_client.bridge_nft(ZK_bridge_on_opBNB_NFT)
        test_client.approve_nft(
            bridge=zk_bridge,
            nft=ZK_bridge_on_opBNB_NFT,
        )

    # Database.create_db()


if __name__ == "__main__":
    main()
