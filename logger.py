import logging
import os
import config

def setup_logger():
    logging.basicConfig(
        filename=os.path.join(config.LOG_DIR, "app.log"),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logger()
