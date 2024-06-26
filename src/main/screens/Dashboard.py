from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import Vertical, Grid
from textual import work
from textual.reactive import reactive

from services.CryptoPriceService import CryptoPriceService


SYMBOLS = [
    "BTC/USD",
    "WBTC/USD",
    "ETH/USD",
    "XRP/USD",
    "USDT/USD",
    "DOT/USD",
    "UNI/USD",
    "DAI/USD",
    "DOGE/USD",
    "BAT/USD",
    "ALGO/USD",
    "MINA/USD",
    "DAI/USDC",
    "AAVE/USD",
    "SUSHI/EUR",
    "SOL/USD",
    "SUSHI/USD",
    "MATIC/USD"
]

_BACKGROUND_COLORS = [
    "#881177",
    "#aa3355",
    "#cc6666",
    "#ee9944",
    "#eedd00",
    "#99dd55",
    "#44dd88",
    "#22ccbb",
    "#00bbcc",
    "#0099cc",
    "#3366bb",
    "#881177",
    "#aa3355",
    "#cc6666",
    "#ee9944",
    "#eedd00",
    "#99dd55",
    "#44dd88",
]

class PriceDisplay(Static):
    """
        Displays and updates the price for each Cryptocurrency
    """

    DEFAULT_CSS = """
    PriceDisplay {
        align: center middle;
        border: heavy white
    }

    #price-container {
       align: center middle
    }

    #prices-container {
        align: center middle;
        grid-size: 2 1;
        padding: 0 1;
    }

    #symbol {
        align: center top;
        text-style: bold;
    }

    #bid {
        align: center middle;
        text-style: bold;
    }

    #ask {
        align: center middle;
        text-style: bold;
    }
    """

    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol
        self.crytpoService = CryptoPriceService()
        self.bid = "0"
        self.ask = "0"

    def compose(self):
        yield Vertical(
            Label(self.symbol, id="symbol"),
            Grid(
                Label(self.bid, id="bid"),
                Label(self.ask, id="ask"),
                id = "prices-container"
            ),
            id = "price-container"
        )

    async def on_mount(self):
        self.update_price()
        self.set_interval(10.0, self.update_price)     

    @work(exclusive=True)
    async def update_price(self):
        bidLabel = self.query_one("#bid")
        askLabel = self.query_one("#ask")
        try:
            price = self.crytpoService.get_price(self.symbol)
            bidLabel.update(str(price['bids'][0][0]))
            askLabel.update(str(price['asks'][0][0]))
        except:
            print("err")
        

class Dashboard(Static):
    """
        Shows a grid with the prices of all the cryptocurrencies
    """

    DEFAULT_CSS = """
    Dashboard {
        align: center middle;
    }

    #dashboard-screen-container {
        grid-size: 3 6;
        padding: 0 1;
        border: thick $background 80%;
        background: $surface;
    }
    """
    def compose(self) -> ComposeResult:
        yield Grid(
            id="dashboard-screen-container"
        )

    def on_mount(self):
        self.load_widgets()

    def load_widgets(self):
        """
            loads all the widgets
        """
        container = self.app.query_one(Grid)
        for i in range (0, len(SYMBOLS)):
            display = PriceDisplay(SYMBOLS[i])
            display.styles.background = f"{_BACKGROUND_COLORS[i]}"
            container.mount(display)



