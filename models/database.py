import json
from typing import List

from loguru import logger

from config import (
    DATABASE_PATH,
    MAX_ATTEMPTS,
    PRIVATE_KEYS_PATH,
    PROXIES_PATH,
    SLEEP_TIME,
    TG_IDS,
    TG_TOKEN,
    USE_PROXY,
)
from utils import read_from_json, read_from_txt, write_to_json

from .chain import bsc


class Database:
    def __init__(
        self,
        sleep_time,
        retry_count,
        use_proxy,
        tg_token,
        tg_ids,
        account_count,
        clients_data: List,
    ) -> None:
        self.sleep_time = sleep_time
        self.retry_count = retry_count
        self.use_proxy = use_proxy
        self.tg_token = tg_token
        self.tg_ids = tg_ids
        self.account_count = account_count
        self.clients_data = clients_data

    def to_dict(self):
        try:
            return json.dumps(self, default=lambda o: o.__dict__)
        except Exception as e:
            logger.exception(f"Database to dict dump error: {e}")

    @staticmethod
    def create_db() -> None:
        from .zk_bridge_client import ZKBridgeClient

        clients_data = []
        wallets = read_from_txt(PRIVATE_KEYS_PATH)
        proxys = read_from_txt(PROXIES_PATH)

        for wallet in wallets:
            wallet_index = wallets.index(wallet)
            proxy = proxys[wallet_index] if USE_PROXY else None
            client = ZKBridgeClient(
                wallet,
                chain=bsc,
                proxy=proxy,
            )

            clients_data.append(client.to_dict())

        account_count = len(clients_data)

        database = Database(
            sleep_time=SLEEP_TIME,
            retry_count=MAX_ATTEMPTS,
            use_proxy=USE_PROXY,
            tg_token=TG_TOKEN,
            tg_ids=TG_IDS,
            account_count=account_count,
            clients_data=clients_data,
        )

        if write_to_json(DATABASE_PATH, database.to_dict()):
            logger.success("Database has been created successfully.")
        else:
            logger.error("Database creation failed.")

    @staticmethod
    def read_db_from_json(db_path):
        read_from_json(DATABASE_PATH)
