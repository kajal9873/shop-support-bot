from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ShopSupportBot"
    app_env: str = "development"
    app_port: int = 8000

    groq_api_key: str = ""
    groq_model: str = "llama3-70b-8192"

    embedding_model: str = "paraphrase-multilingual-MiniLM-L12-v2"

    chroma_persist_dir: str = "./data/chroma_db"
    chroma_collection_name: str = "shop_faq_catalog"

    database_url: str = "sqlite:///./data/shop.db"

    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()