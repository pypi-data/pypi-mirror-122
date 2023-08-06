"""Project entry file."""
__version__ = "1.0.4"
__all__ = ["api"]

from serifan import session


def api():
    """Entry function for access to the Shortboxed api."""
    return session.Session()
