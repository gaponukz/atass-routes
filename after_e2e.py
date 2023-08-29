from src.infrastructure.settings import settings
from src.infrastructure.db.mongodb import RouteRepository
config = settings.EnvSettingsExporter().load()

db = RouteRepository(config.mongodb_url, 'test')
db.clear()
