from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_host: str = "127.0.0.1"
    app_port: int = 8765
    database_path: str = "./data/kitsune.db"
    ollama_base_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5:3b"
    google_client_secret_file: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
