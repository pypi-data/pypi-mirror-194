"""
api settings
"""
from pydantic import BaseSettings


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Spotlight settings module
    settings will be loaded from env variables or .env file
    """

    dev: bool = False
    license_path = "renumics_license.key"

    class Config:
        """
        settings config
        set env prefix to spotlight_
        """

        env_prefix = "spotlight_"


settings = Settings()
