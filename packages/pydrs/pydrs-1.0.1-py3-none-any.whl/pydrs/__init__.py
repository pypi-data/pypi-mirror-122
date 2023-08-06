import logging as _logging
import typing as _typing

__author__ = ""
__version__ = "1.0.1"
__date__ = "Wed, 06 Oct 2021 17:38:48 +0000"

def get_logger(
    name=__file__,
    level: int = _logging.INFO,
    handlers: _typing.Optional[_typing.List[_logging.Handler]] = None,
) -> _logging.Logger:
    """Returns a logger object"""

    logger = _logging.getLogger(name)

    if not len(logger.handlers) and not handlers:
        formatter = _logging.Formatter(
            "[%(asctime)s %(levelname)s %(filename)s:%(lineno)s - %(funcName)s] %(message)s"
        )
        logger.setLevel(level)
        console = _logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
    return logger
