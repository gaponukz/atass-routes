import os
import dataclasses
from dotenv import load_dotenv

@dataclasses.dataclass
class Settings:
    gmail: str
    gmail_password: str
    rabbitmq_url: str
    mongodb_url: str

class EnvSettingsExporter:
    def __init__(self):
        load_dotenv()

    def load(self) -> Settings:
        return Settings(
            rabbitmq_url=os.getenv("rabbitmq_url") or os.getenv("rabbitmqUrl") or '',
            mongodb_url=os.getenv("mongodb_url") or os.getenv("mongodbUrl") or '',
            gmail=os.getenv("gmail") or '',
            gmail_password=os.getenv("gmail_password") or os.getenv("gmailPassword") or '',
        )
