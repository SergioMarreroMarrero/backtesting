import logging

LOG_FORMAT = "%(asctime)s %(levelname)s :: %(message)s"

my_stream_handler = logging.StreamHandler()
my_stream_handler.setLevel(logging.INFO)  # Solo INFO o superior
my_stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))  # Asegurar formato

# Global logger configuration
logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler("app.log"),
        my_stream_handler
    ]
)

logger = logging.getLogger()
