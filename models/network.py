class Network:
    def __init__(
        self,
        name: str,
        rpc: str,
        chain_id: int,
        eip1559_tx: bool,
        coin_symbol: str,
        explorer: str,
        decimals: int = 18,
    ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_tx = eip1559_tx
        self.coin_symbol = coin_symbol
        self.decimals = decimals
        self.explorer = explorer

    def __str__(self):
        return f"{self.name}"


Polygon = Network(
    name="polygon",
    rpc="https://polygon-rpc.com/",
    chain_id=137,
    eip1559_tx=True,
    coin_symbol="MATIC",
    explorer="https://polygonscan.com/",
)


BSC = Network(
    name="bsc",
    rpc="https://rpc.ankr.com/bsc",
    chain_id=56,
    eip1559_tx=True,
    coin_symbol="BNB",
    explorer="https://bscscan.com/",
)


Core = Network(
    name="core",
    rpc="https://rpc.coredao.org",
    chain_id=1116,
    eip1559_tx=True,
    coin_symbol="CORE",
    explorer="https://scan.coredao.org/",
)


Celo = Network(
    name="celo",
    rpc="https://rpc.ankr.com/celo",
    chain_id=42220,
    eip1559_tx=True,
    coin_symbol="CELO",
    explorer="https://celoscan.io/",
)


Arbitrum = Network(
    name="arbitrum",
    rpc="https://rpc.ankr.com/arbitrum/",
    chain_id=42161,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://arbiscan.io/",
)


Optimism = Network(
    name="optimism",
    rpc="https://rpc.ankr.com/optimism/",
    chain_id=10,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://optimistic.etherscan.io/",
)


Avalanche = Network(
    name="avalanche",
    rpc="https://rpc.ankr.com/avalanche/",
    chain_id=43114,
    eip1559_tx=True,
    coin_symbol="AVAX",
    explorer="https://snowtrace.io/",
)


Fantom = Network(
    name="fantom",
    rpc="https://rpc.ankr.com/fantom/",
    chain_id=250,
    eip1559_tx=True,
    coin_symbol="FTM",
    explorer="https://ftmscan.com/",
)


opBNB = Network(
    name="opBNB",
    rpc="https://opbnb-testnet-rpc.bnbchain.org",
    chain_id=5611,
    eip1559_tx=True,
    coin_symbol="tBNB",
    explorer="https://opbnbscan.com/",
)


combo = Network(
    name="combo",
    rpc="https://test-rpc.combonetwork.io",
    chain_id=91715,
    eip1559_tx=True,
    coin_symbol="tcBNB",
    explorer="https://combotrace-testnet.nodereal.io/",
)


nova = Network(
    name="nova",
    rpc="https://nova.arbitrum.io/rpc",
    chain_id=42170,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://nova.arbiscan.io/",
)


moonbeam = Network(
    name="moonbeam",
    rpc="https://rpc.ankr.com/moonbeam",
    chain_id=1284,
    eip1559_tx=True,
    coin_symbol="GLMR",
    explorer="https://moonscan.io/",
)


gnosis = Network(
    name="gnosis",
    rpc="https://rpc.ankr.com/gnosis",
    chain_id=100,
    eip1559_tx=True,
    coin_symbol="XDAI",
    explorer="https://gnosisscan.io/",
)


metis = Network(
    name="metis",
    rpc="https://andromeda.metis.io/?owner=1088",
    chain_id=1088,
    eip1559_tx=True,
    coin_symbol="METIS",
    explorer="https://andromeda-explorer.metis.io/",
)
