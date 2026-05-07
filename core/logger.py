import logging
import os
from core.config import LOG_DIR

def setup_logger():
    log_file = os.path.join(LOG_DIR, "app.log")
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logger()

