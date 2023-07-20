from nfts import NFTs


class NFT:
    def __init__(self, name, chains, contract_chain_mapping) -> None:
        self.name = None
        self.chains = None
        self.contract_to_chain_mapping = None

    @staticmethod
    def create_nft_obj(nft_name):
        if nft_name in NFTs:
            nft_data = NFTs[nft_name]
            chains = nft_data.get("chains", [])
            contract_to_chain_mapping = nft_data.get("contracts", {})
