import logging
from logging.handlers import TimedRotatingFileHandler

import uvicorn

from src import create_app

logging.basicConfig(
    level=logging.DEBUG,
    handlers=[
        TimedRotatingFileHandler(
            "logs/system.log", when="midnight", interval=1
        ),
        logging.StreamHandler(),
    ],
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logging.getLogger("sqlalchemy").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=9010)
