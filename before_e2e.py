from src.infrastructure.settings import settings
from src.infrastructure.db.mongodb import RouteRepository
from src.infrastructure.db.json_db import RouteRepository as JsonRouteRepository
config = settings.EnvSettingsExporter().load()

db = RouteRepository(config.mongodb_url, 'test')

db.clear()
db.create(JsonRouteRepository("routes.json").read_all()[0])
