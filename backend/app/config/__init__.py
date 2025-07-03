# File: backend/app/config/__init__.py

import os

from .development import Config as DevConfig
from .production import Config as ProdConfig
from .testing import Config as TestConfig


def get_config(env: str = None):
    """
    Returns the appropriate Config class based on the given environment.
    :param env: str - Environment name ('development', 'production', 'testing')
    :return: Config class
    """
    env = env or os.getenv("FLASK_ENV", "development").lower()

    if env == "production":
        return ProdConfig
    elif env == "testing":
        return TestConfig
    return DevConfig


# Optionally expose configs via a dict (alternative usage pattern)
config_by_name = {
    "development": DevConfig,
    "production": ProdConfig,
    "testing": TestConfig
}
