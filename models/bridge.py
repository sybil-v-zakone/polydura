from config import LZ_BRIDGE_ABI, ZK_BRIDGE_ABI
from utils import read_from_json


class Bridge:
    def __init__(
        self,
        name,
        abi,
        chain_to_contract_mapping: str,
    ) -> None:
        self.name = name
        self.abi = abi
        self.chain_to_contract_mapping = chain_to_contract_mapping

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "contract_to_chain_mapping": self.chain_to_contract_mapping,
        }


zk_bridge = Bridge(
    name="ZK Bridge",
    abi=read_from_json(ZK_BRIDGE_ABI),
    chain_to_contract_mapping={
        "bsc": "0xE09828f0DA805523878Be66EA2a70240d312001e",
    },
)

lz_bridge = Bridge(
    name="LZ Bridge",
    abi=read_from_json(LZ_BRIDGE_ABI),
    chain_to_contract_mapping={},
)
