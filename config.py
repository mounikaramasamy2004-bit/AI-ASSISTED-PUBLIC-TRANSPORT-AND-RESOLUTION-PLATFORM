"""Application configuration. Everything can be overridden with environment variables."""
import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production-0123456789")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key-change-in-production-0123456789")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=12)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(BASE_DIR, "transport.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # "*" is fine for local development. In production set e.g. "https://yourdomain.com".
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
    # Registering as ADMIN needs this invite code (prevents anyone from self-promoting to admin).
    ADMIN_REGISTRATION_CODE = os.environ.get("ADMIN_REGISTRATION_CODE", "ADMIN-2026")
    JSON_SORT_KEYS = False
