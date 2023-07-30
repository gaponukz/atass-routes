import os
import dataclasses
from dotenv import load_dotenv

@dataclasses.dataclass
class Settings:
    rabbitmq_url: str
    mongodb_url: str

class EnvSettingsExporter:
    def __init__(self):
        load_dotenv()

    def load(self) -> Settings:
        return Settings(
            rabbitmq_url=os.getenv("rabbitmq_url"),
            mongodb_url=os.getenv("mongodb_url")
        )
