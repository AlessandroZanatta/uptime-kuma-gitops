import logging
import os

from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler()],
)

log = logging.getLogger("rich")
