import logging
from pathlib import Path

from config.settings import LOG_DIR

LOG_FILE = LOG_DIR / "pipeline.log"

LOG_FILE.parent.mkdir(
    parents=True, 
    exist_ok=True
    )

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
