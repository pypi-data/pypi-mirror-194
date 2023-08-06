import datetime
import logging
from pathlib import Path

import colorlog

from . import dev_tools, feat_analysis, modelling

# Create logs folder if it does not exists
if not Path("./logs").exists():
    Path("./logs").mkdir()
    print(f"Created directory for logs at '{Path('./logs').resolve()}'")

# Set up root logger, and add a file handler to root logger
logging.basicConfig(
    filename=f"./logs/log_{datetime.datetime.now().strftime('%Y-%m-%d_%H:%M')}.log",
    level=logging.DEBUG,
    format="[%(levelname)1.1s %(asctime)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Create logger for handling stream
shandler = colorlog.StreamHandler()
shandler.setFormatter(
    colorlog.ColoredFormatter(
        "%(log_color)s[%(levelname)1.1s %(asctime)s]%(reset)s %(message)s",
        "%Y-%m-%d %H:%M:%S",
    )
)
stream_logger = colorlog.getLogger("stream")
stream_logger.addHandler(shandler)
