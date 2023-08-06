"""Log mixin module.

Defines a log mixin class allowing classes to get a logger with the name of the module,
class and method it was called from.

"""
import inspect
import logging
from types import FrameType


class LogMixin(object):
    """Log mixin class.

    Adds a method to classes that returns a logger whose name is
    {module}.{class}.{method}.

    """
    @staticmethod
    def get_logger() -> logging.Logger:
        """Returns a logger whose name is {module}.{class}.{method}."""
        f: FrameType | None = inspect.currentframe().f_back

        if isinstance(f, FrameType):

            a: str = f.f_globals["__name__"]
            try:
                b: str = f.f_locals["self"].__class__.__name__
            except KeyError:
                try:
                    b: str = f.f_locals["cls"].__name__
                except KeyError:
                    b: str = "unknown"
            c: str = f.f_code.co_name
            return logging.getLogger(f"{a}.{b}.{c}")

        else:

            logger: logging.Logger = logging.getLogger(__name__)
            logger.warning("Could not get logger name from frame; using __name__.")
            return logger
