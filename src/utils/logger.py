import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOG_DIR = PROJECT_ROOT / "logs"

LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "pipeline.log"


def logger():
    logging.basicConfig(

        level=logging.INFO,

        format="%(asctime)s | %(levelname)s | %(message)s",

        handlers=[

            logging.FileHandler(LOG_FILE),

            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)