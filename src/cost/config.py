from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_path: str = "artifact/cost_model.joblib" #плохо!!!! (веса модели в mlflow/dvc)
    database_url: str | None = None
    log_level: str = "INFO"

    model_config = {"env_file": ".env"}

settings = Settings()