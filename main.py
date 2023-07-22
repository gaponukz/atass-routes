from fastapi import FastAPI
from src.db.json_db import RouteRepository
from src.usecases.view_routes import ViewRoutesUseCase
from src.usecases.route_availability import RouteAvailabilityUseCase
from src.usecases.add_routes import AddRoutesUseCase

from src.handlers.add_routes import AddRoutesHandler
from src.handlers.route_availability import RouteAvailabilityHandler
from src.handlers.view_routes import ViewRoutesHandler

db = RouteRepository("routes.json")
view_usecase = ViewRoutesUseCase(db)
availability_usecase = RouteAvailabilityUseCase(db)
add_routes_usecase = AddRoutesUseCase(db)

add_routes_handler = AddRoutesHandler(add_routes_usecase)
availability_handler = RouteAvailabilityHandler(availability_usecase)
view_handler = ViewRoutesHandler(view_usecase)

app = FastAPI()
app.include_router(view_handler.router)
app.include_router(availability_handler.router)
app.include_router(add_routes_handler.router)
