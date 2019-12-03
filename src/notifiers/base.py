class BaseNotifier:
    """Base notifier class."""

    def notify(self, message):
        """
        Base method for sending notifications.
        Must be implemented in inherited classes.
        """

        raise NotImplementedError("Implement this method in an inherited class")
