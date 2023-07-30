import json
import random
from typing import List

from fake_useragent import UserAgent
from loguru import logger

from config import DATABASE_PATH, PRIVATE_KEYS_PATH, PROXIES_PATH, USE_PROXY
from utils import read_from_json, read_from_txt, write_to_json

from .chain import bsc


class Database:
    def __init__(
        self,
        account_count,
        unfinished_accounts: List,
        finished_accounts: List,
        accounts_without_balance: List,
    ) -> None:
        self.account_count = account_count
        self.unfinished_accounts = unfinished_accounts
        self.finished_accounts = finished_accounts
        self.accounts_without_balance = accounts_without_balance

    def to_dict(self):
        try:
            return json.dumps(self, default=lambda o: o.__dict__)
        except Exception as e:
            logger.exception(f"Database to dict dump error: {e}")

    @staticmethod
    def create_db() -> None:
        from .zk_bridge_client import ZKBridgeClient

        unfinished_accounts = []
        finished_accounts = []
        accounts_without_balance = []

        wallets = read_from_txt(PRIVATE_KEYS_PATH)
        proxys = read_from_txt(PROXIES_PATH)

        for wallet in wallets:
            wallet_index = wallets.index(wallet)
            proxy = proxys[wallet_index] if USE_PROXY else None
            user_agent = UserAgent().random
            client = ZKBridgeClient(
                wallet,
                chain=bsc,
                proxy=proxy,
                user_agent=user_agent,
            )

            unfinished_accounts.append(client.to_dict())

        account_count = len(unfinished_accounts)

        database = Database(
            account_count=account_count,
            unfinished_accounts=unfinished_accounts,
            finished_accounts=finished_accounts,
            accounts_without_balance=accounts_without_balance,
        )

        if write_to_json(DATABASE_PATH, database.to_dict()):
            logger.success("Database has been created successfully.")
        else:
            logger.error("Database creation failed.")

    @staticmethod
    def read_db_from_json(db_path=DATABASE_PATH):
        db = read_from_json(db_path)
        return Database(
            db["account_count"],
            db["unfinished_accounts"],
            db["finished_accounts"],
            db["accounts_without_balance"],
        )

    def get_random_unfinished_account(self):
        logger.info("Getting a random client.")
        if self.unfinished_accounts:
            random_index = random.randrange(len(self.unfinished_accounts))
            logger.info("Client chosen.")
            return random_index, self.unfinished_accounts[random_index]
        else:
            logger.warning("No unfinished accounts available in the database.")
            exit()

    def update_db(self):
        if write_to_json(DATABASE_PATH, self.to_dict()):
            logger.success("Database updated successfully.")
        else:
            logger.error("Failed to update the database.")
