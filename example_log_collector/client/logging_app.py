import logging
import time
import random


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - lvl=%(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("my_app")


levels = [
    logging.DEBUG,
    logging.INFO,
    logging.WARNING,
    logging.ERROR,
    logging.CRITICAL
]

messages = {
    logging.DEBUG: "Debug message",
    logging.INFO: "Info message",
    logging.WARNING: "Warning message",
    logging.ERROR: "Error message",
    logging.CRITICAL: "Critical message"
}

def generate_logs():
    while True:
        level = random.choice(levels)
        logger.log(level, messages[level])
        time.sleep(random.uniform(0.5, 2))

if __name__ == "__main__":
    logger.info("Starting logging application...")
    try:
        generate_logs()
    except KeyboardInterrupt:
        logger.info("Stopping logging application...")