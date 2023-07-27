class Chain:
    def __init__(
        self,
        name: str,
        rpc: str,
        chain_id: int,
        eip1559_tx: bool,
        coin_symbol: str,
        explorer: str,
        decimals: int = 18,
        supports_lz: bool = False,
        lz_chain_id: int | None = None,
        zk_chain_id: int | None = None,
    ):
        self.name = name
        self.rpc = rpc
        self.chain_id = chain_id
        self.eip1559_tx = eip1559_tx
        self.coin_symbol = coin_symbol
        self.decimals = decimals
        self.explorer = explorer
        self.supports_lz = supports_lz
        self.lz_chain_id = lz_chain_id
        self.zk_chain_id = zk_chain_id

    def __str__(self):
        return f"{self.name}"

    def __dict__(self):
        return {
            "name": self.name,
            "rpc": self.rpc,
            "chain_id": self.chain_id,
            "coin_symbol": self.coin_symbol,
            "supports_lz": self.supports_lz,
            "lz_chain_id": self.lz_chain_id,
            "zk_chain_id": self.zk_chain_id,
        }


polygon = Chain(
    name="polygon",
    rpc="https://polygon-rpc.com/",
    chain_id=137,
    eip1559_tx=True,
    coin_symbol="MATIC",
    explorer="https://polygonscan.com/",
    supports_lz=True,
    lz_chain_id=109,
    zk_chain_id=4,
)


bsc = Chain(
    name="bsc",
    rpc="https://rpc.ankr.com/bsc",
    chain_id=56,
    eip1559_tx=False,
    coin_symbol="BNB",
    explorer="https://bscscan.com/",
    supports_lz=True,
    lz_chain_id=102,
    zk_chain_id=3,
)


core = Chain(
    name="core",
    rpc="https://rpc.coredao.org",
    chain_id=1116,
    eip1559_tx=False,
    coin_symbol="CORE",
    explorer="https://scan.coredao.org/",
    supports_lz=True,
    lz_chain_id=153,
    zk_chain_id=17,
)


celo = Chain(
    name="celo",
    rpc="https://rpc.ankr.com/celo",
    chain_id=42220,
    eip1559_tx=True,
    coin_symbol="CELO",
    explorer="https://celoscan.io/",
    supports_lz=True,
    lz_chain_id=125,
    zk_chain_id=18,
)


arbitrum = Chain(
    name="arbitrum",
    rpc="https://rpc.ankr.com/arbitrum/",
    chain_id=42161,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://arbiscan.io/",
    supports_lz=True,
    lz_chain_id=110,
)


optimism = Chain(
    name="optimism",
    rpc="https://rpc.ankr.com/optimism/",
    chain_id=10,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://optimistic.etherscan.io/",
    supports_lz=True,
    lz_chain_id=111,
)


avalanche = Chain(
    name="avalanche",
    rpc="https://rpc.ankr.com/avalanche/",
    chain_id=43114,
    eip1559_tx=True,
    coin_symbol="AVAX",
    explorer="https://snowtrace.io/",
    supports_lz=True,
    lz_chain_id=106,
)


fantom = Chain(
    name="fantom",
    rpc="https://rpc.ankr.com/fantom/",
    chain_id=250,
    eip1559_tx=False,
    coin_symbol="FTM",
    explorer="https://ftmscan.com/",
    supports_lz=True,
    lz_chain_id=112,
    zk_chain_id=6,
)


opBNB = Chain(
    name="opBNB",
    rpc="https://opbnb-testnet-rpc.bnbchain.org",
    chain_id=5611,
    eip1559_tx=True,
    coin_symbol="tBNB",
    explorer="https://opbnbscan.com/",
    supports_lz=False,
    zk_chain_id=116,
)


combo = Chain(
    name="combo",
    rpc="https://test-rpc.combonetwork.io",
    chain_id=91715,
    eip1559_tx=True,
    coin_symbol="tcBNB",
    explorer="https://combotrace-testnet.nodereal.io/",
    supports_lz=False,
    zk_chain_id=114,
)


nova = Chain(
    name="nova",
    rpc="https://nova.arbitrum.io/rpc",
    chain_id=42170,
    eip1559_tx=True,
    coin_symbol="ETH",
    explorer="https://nova.arbiscan.io/",
    supports_lz=True,
    lz_chain_id=175,
    zk_chain_id=14,
)


moonbeam = Chain(
    name="moonbeam",
    rpc="https://rpc.ankr.com/moonbeam",
    chain_id=1284,
    eip1559_tx=True,
    coin_symbol="GLMR",
    explorer="https://moonscan.io/",
    supports_lz=True,
    lz_chain_id=126,
    zk_chain_id=9,
)


gnosis = Chain(
    name="gnosis",
    rpc="https://rpc.ankr.com/gnosis",
    chain_id=100,
    eip1559_tx=True,
    coin_symbol="XDAI",
    explorer="https://gnosisscan.io/",
    supports_lz=True,
    lz_chain_id=145,
)


metis = Chain(
    name="metis",
    rpc="https://andromeda.metis.io/?owner=1088",
    chain_id=1088,
    eip1559_tx=True,
    coin_symbol="METIS",
    explorer="https://andromeda-explorer.metis.io/",
    supports_lz=True,
    lz_chain_id=151,
)

source_chains = [
    polygon,
    bsc,
    core,
    celo,
]

destination_chains = [
    celo,
    arbitrum,
    avalanche,
    fantom,
    opBNB,
    optimism,
    metis,
    gnosis,
    moonbeam,
    nova,
    combo,
]
