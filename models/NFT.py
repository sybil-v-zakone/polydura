from typing import Tuple

from .network import Network


class NFT:
    def __init__(
        self,
        name,
        mint_chains: Tuple[Network],
        contract_chain_mapping: dict,
        abi,
    ) -> None:
        self.name = name
        self.mint_chains = mint_chains
        self.contract_to_chain_mapping = contract_chain_mapping
        self.abi = abi
