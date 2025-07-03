# File: backend/app/config/testing.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'test-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///:memory:')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-test')
    DEBUG = False
    TESTING = True
    ENV = "testing"

    # Mock mail settings
    MAIL_SERVER = "localhost"
    MAIL_PORT = 8025
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""

    # Celery config (mocked or dev-compatible)
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"

    # Test upload path
    MEDIA_UPLOAD_PATH = "./test_uploads"
