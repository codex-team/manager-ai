from src.notifiers.base import BaseNotifier


class StdoutNotifier(BaseNotifier):
    """Notifier class for sending messages to stdout."""

    def notify(self, message):
        """Simple notification method. Sends message to stdout."""
        print(message)
