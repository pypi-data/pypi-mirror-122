from .client import get_client  # noqa

with open("version") as f:
    __version__ = f.read().strip()
