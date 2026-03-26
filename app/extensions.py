from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging
from logging.handlers import TimedRotatingFileHandler
import os

# Initialize extension instances
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def setup_logging(app):
    """
    Configure daily rotating logs under /logs/auth.log
    """
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    log_file = os.path.join(logs_dir, "auth.log")

    # Avoid attaching multiple handlers during reload
    if not any(isinstance(h, TimedRotatingFileHandler) for h in app.logger.handlers):
        handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=30,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)

        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)
