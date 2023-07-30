from loguru import logger

from config import DATABASE_PATH
from models.database import Database
from models.zk_bridge_client import ZKBridgeClient


def messenger():
    try:
        database = Database.read_db_from_json(db_path=DATABASE_PATH)
        item_index, db_item = database.get_random_unfinished_account()

        try:
            client = ZKBridgeClient.client_from_db_item(db_item=db_item)
            client.load_profile()

            if not database.unfinished_accounts:
                logger.success("All messages were sent.")
                exit()

            message_status = client.send_message()

            if message_status:
                database.finished_accounts.append(client.to_dict())
                database.unfinished_accounts.pop(item_index)
                database.update_db()

            messenger()

        except Exception as e:
            logger.exception(f"Exception in full warmup mode: {e}")
    except Exception as e:
        logger.exception("An error occurred when doing full warmup.")
