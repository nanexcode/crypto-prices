from textual.app import App, ComposeResult
from textual.widgets import Footer, Header
from textual.binding import Binding
from screens.modals.HelpScreen import HelpScreen
from screens.modals.WelcomeModal import WelcomeModal
from screens.Dashboard import Dashboard

class CryptoPrices(App):
    """A class representing a trading application."""

    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="question_mark", action="get_help", description="Show help screen", key_display="?"),
    ]

    def compose(self) -> ComposeResult:
        """Create the app layout and widgets."""
        yield Header(show_clock=True)
        yield Footer()
        yield Dashboard()

    def action_get_help(self) -> None:
        self.push_screen(HelpScreen())


if __name__ == '__main__':
    CryptoPrices().run()
