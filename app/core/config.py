import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

from functools import lru_cache


load_dotenv()


class Settings(BaseSettings):
    

    ENV: str = os.getenv("ENVIRONMENT", "dev")

    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_HOST: str = ""
    POSTGRES_PORT: str = ""
    POSTGRES_DB: str = ""
    POSTGRES_DB_URL: str = ""


    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""

    ## model_ids
    BEDROCK_MODEL_ID: str = ""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.secrets_manager_client = None
        self._load_config()
    
    def _load_config(self):
        if self.ENV == "prod":
            self._load_from_secrets_manager()
        else:
            self._load_from_env()
        
        self._post_load_validation()
    
    def _load_from_secrets_manager(self):
        print("Loading the variables from AWS Secrets Manager")
        pass
    
    def _load_from_env(self):
        print("Loading the variables from environment variables")

        self.ENV = os.getenv("ENVIRONMENT", "dev")

        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")

        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")

        self.BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL")

    def _post_load_validation(self):

        if self.ENV == "prod":
            self._validate_prod_env()
        

        if not self.POSTGRES_DB_URL and all([self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_PORT, self.POSTGRES_DB]):
            self.POSTGRES_DB_URL = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    def _validate_prod_env(self):
        pass


@lru_cache()
def get_settings() -> Settings:
    return Settings()