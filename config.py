import os
from dotenv import load_dotenv

path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(path)

class Config(object):
    DEBUG = False
    TESTING = False
    DB_PATH = os.getenv("SQLITE_PATH", "")
    API_URL = os.getenv("API_URL", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    JWT_SECRET = os.getenv("JWT_SECRET", "")

class ProductionConfig(Config):
    DB_PATH = env_var = os.getenv("SQLITE_PATH", "")

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DB_PATH = env_var = os.getenv("TEST_SQLITE_PATH", "")

def get_config():
    """Get config class depending on env-variable. Default production."""
    env_var = os.getenv("FLASK_ENV")

    if env_var == "development":
        return DevelopmentConfig
    elif env_var == "test":
        return TestingConfig

    return ProductionConfig
