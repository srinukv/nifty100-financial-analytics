import logging
from pathlib import Path

LOG_DIR = Path("output/ratio_logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "day08_profitability.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

ratio_logger = logging.getLogger("ratio_engine")