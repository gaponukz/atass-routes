import sys
from src.infrastructure.db.mongodb import RouteRepository
from src.infrastructure.db.json_db import RouteRepository as JsonRouteRepository

db = RouteRepository(sys.argv[1], "Cluster0")

db.clear()
db.create(JsonRouteRepository("routes.json").read_all()[0])
