import logging
import os
import sys
from analytics_worker.config import Config
from analytics_worker.worker import Worker

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    try:
        config = Config()
        worker = Worker(config)
        worker.start()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()