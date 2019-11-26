from src.transports.base import BaseNotifier


class StdoutNotifier(BaseNotifier):
    """Notifier class for sending messages to stdout."""

    @staticmethod
    def notify(message):
        """Simple notification method. Sends message to stdout."""
        print(message)
