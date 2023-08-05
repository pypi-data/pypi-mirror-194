"""System Module."""

import os


class System(object):
    """
    System methods.

    For now only envirnoment vars.
    """

    @staticmethod
    def setenv(name: str, val: str) -> None:
        """Set environment variable."""
        os.environ[name] = val

    @staticmethod
    def getenv(name: str) -> str:
        """Get environment variable."""

        return os.environ[name] if name in os.environ.keys() else ""
