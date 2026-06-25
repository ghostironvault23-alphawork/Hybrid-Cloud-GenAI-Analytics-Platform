from functools import lru_cache
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field(default="Hybrid Cloud GenAI Analytics Platform", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    api_key: str = Field(default="dev-demo-key", alias="API_KEY")
    local_data_dir: str = Field(default="backend/runtime/data_lake", alias="LOCAL_DATA_DIR")
    sqlite_db_path: str = Field(default="backend/runtime/transactions.db", alias="SQLITE_DB_PATH")
    use_bedrock: bool = Field(default=False, alias="USE_BEDROCK")
    aws_region: str = Field(default="us-east-1", alias="AWS_REGION")
    bedrock_model_id: str = Field(
        default="anthropic.claude-3-haiku-20240307-v1:0",
        alias="BEDROCK_MODEL_ID",
    )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def data_path(self) -> Path:
        return Path(self.local_data_dir)

    @property
    def db_path(self) -> Path:
        return Path(self.sqlite_db_path)


@lru_cache
def get_settings() -> Settings:
    return Settings()
