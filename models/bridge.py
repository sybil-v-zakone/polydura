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
        "polygon": "0x2E953a70C37E8CB4553DAe1F5760128237c8820D",
        "core": "0x5c5979832A60c17bB06676fa906bEdD1A013e18c",
        "celo": "0x24339b7f8d303527C8681382AbD4Ec299757aF63",
    },
)

lz_bridge = Bridge(
    name="LZ Bridge",
    abi=read_from_json(LZ_BRIDGE_ABI),
    chain_to_contract_mapping={
        "bsc": "0x3668c325501322CEB5a624E95b9E16A019cDEBe8",
        "polygon": "0xFFdF4Fe05899C4BdB1676e958FA9F21c19ECB9D5",
        "core": "0x3701c5897710F16F1f75c6EaE258bf11Ee189a5d",
        "celo": "0xe47b0a5F2444F9B360Bd18b744B8D511CfBF98c6",
    },
)
