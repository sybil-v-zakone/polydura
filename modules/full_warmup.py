from loguru import logger

from config import DATABASE_PATH
from models.database import Database
from models.NFT import NFT
from models.zk_bridge_client import ZKBridgeClient


def full_warmup():
    try:
        database = Database.read_db_from_json(db_path=DATABASE_PATH)
        item_index, db_item = database.get_random_unfinished_account()

        try:
            client = ZKBridgeClient.client_from_db_item(db_item=db_item)
            client.load_profile()

            if not client.nfts_to_mint:
                database.finished_accounts.append(client.to_dict())
                database.unfinished_accounts.pop(item_index)
                database.update_db()

                if not database.unfinished_accounts:
                    logger.success("All accounts are warmed up.")
                    exit()

                full_warmup()

            nft = client.mint_random_nft()

            if isinstance(nft, NFT):
                database.update_db()

            elif nft is None:
                database.update_db()
                full_warmup()

            elif nft is False:
                database.accounts_without_balance.append(client.to_dict())
                database.unfinished_accounts.pop(item_index)
                database.update_db()

                full_warmup()

            nft = client.bridge_nft(nft=nft)

            if isinstance(nft, NFT):
                database.update_db()

            if nft is False:
                database.accounts_without_balance.append(client.to_dict())
                database.unfinished_accounts.pop(item_index)
                database.update_db()

                full_warmup()
            if nft is None:
                database.update_db()
                full_warmup()

        except Exception as e:
            logger.exception(f"Exception in full warmup mode: {e}")
        full_warmup()
    except Exception as e:
        logger.exception("An error occurred when doing full warmup.")
