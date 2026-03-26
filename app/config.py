import os


class Config:
    """
    Unified configuration for:
    - Local development (SQLite)
    - Production on Render + Neon PostgreSQL
    """

    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")

    # -------------------------------------------------
    # DATABASE
    # -------------------------------------------------
    # Local:
    #   sqlite:///auth.db
    # Production (Render):
    #   DATABASE_URL = postgresql://... (Neon)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///auth.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------------------------------
    # ✅ CRITICAL FIX FOR RENDER + NEON (SSL DISCONNECT)
    # -------------------------------------------------
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,   # Reconnect if SSL connection dropped
        "pool_recycle": 300,     # Recycle connections every 5 minutes
    }
