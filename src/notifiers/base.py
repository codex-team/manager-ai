class BaseNotifier:
    """Base notifier class."""

    @staticmethod
    def notify(message):
        """
        Base method for sending notifications.
        Must be implemented in inherited classes.
        """

        raise NotImplementedError("Implement this method in an inherited class")
