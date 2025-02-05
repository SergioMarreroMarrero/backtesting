import logging

LOG_FORMAT = "%(asctime)s %(levelname)s :: %(message)s"

# Global logger configuration
logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()
