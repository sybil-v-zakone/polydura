from loguru import logger

from config import DATABASE_PATH
from models.database import Database
from models.zk_bridge_client import ZKBridgeClient


def full_warmup():
    try:
        database = Database.read_db_from_json(db_path=DATABASE_PATH)
        item_index, db_item = database.get_random_unfinished_account()

        try:
            client = ZKBridgeClient.client_from_db_item(db_item=db_item)
            client.load_profile()

            nft = client.mint_random_nft()
            if nft is None:
                full_warmup()
            client.bridge_nft(nft=nft)
        except Exception as e:
            logger.exception(f"Exception in full warmup mode: {e}")
        full_warmup()
    except Exception as e:
        pass
