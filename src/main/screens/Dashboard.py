from textual.app import ComposeResult
from textual.widgets import Static, Label
from textual.containers import Vertical, Grid
from textual import work
from services.CryptoPriceService import CryptoPriceService
import time
import random

SYMBOLS = [
    "BTC/USD", 
    "ETH/USD", 
    "SOL/USD", 
    "BNB/USD", 
    "MATIC/USD",
    "USDC/USD", 
    "DAI/USD", 
    "USDT/USD",
    "USDT/USD",
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
    "#663399",
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
        self.bid = "$ 72345.00"
        self.ask = "$ 72350.00"

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
        self.set_interval(2.0, self.update_price)

    @work(exclusive=True)
    async def update_price(self):
        bidLabel = self.query_one("#bid")
        askLabel = self.query_one("#ask")
        try:
            price = self.crytpoService.getPrice(self.symbol)
            bidLabel.update(str(price['bids'][0][0]))
            askLabel.update(str(price['asks'][0][0]))
        except:
            bidLabel.update("UNK")
            askLabel.update("UNK")
        

class Dashboard(Static):
    """
        Shows a grid with the prices of all the cryptocurrencies
    """

    DEFAULT_CSS = """
    Dashboard {
        align: center middle;
    }

    #dashboard-screen-container {
        grid-size: 3 3;
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



