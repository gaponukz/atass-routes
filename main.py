from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.settings import settings
from src.db.json_db import RouteRepository
from src.logger.console import ConsoleLogger
from src.usecases.view_routes import ViewRoutesUseCase
from src.usecases.route_availability import RouteAvailabilityUseCase
from src.usecases.add_routes import AddRoutesUseCase
from src.usecases.edit_routes import EditRoutersUseCase
from src.usecases.delete_route import DeleteRouteUseCase
from src.usecases.add_passenger import AddPassengerUseCase
from src.handlers.change_routes import ChangeRoutesHandler
from src.handlers.add_routes import AddRoutesHandler
from src.handlers.route_availability import RouteAvailabilityHandler
from src.handlers.view_routes import ViewRoutesHandler
from src.handlers.add_passenger import RoutesEventsListener

from src.logger.decorators.add_passenger import AddPassengerLogger
from src.logger.decorators.add_routes import AddRoutesLogger
from src.logger.decorators.delete_route import DeleteRouteLogger
from src.logger.decorators.edit_route import EditRouteLogger
from src.logger.decorators.route_availability import AvailabilityServiceLogger
from src.logger.decorators.view_routes import ViewServiceLogger

db = RouteRepository("routes.json")
config = settings.EnvSettingsExporter().load()
logger = ConsoleLogger()

view_usecase = ViewServiceLogger(ViewRoutesUseCase(db), logger)
availability_usecase = AvailabilityServiceLogger(RouteAvailabilityUseCase(db), logger)
add_routes_usecase = AddRoutesLogger(AddRoutesUseCase(db), logger)
edit_routers_usecase = EditRouteLogger(EditRoutersUseCase(db), logger)
delete_route_usecase = DeleteRouteLogger(DeleteRouteUseCase(db), logger)
add_passenger_usecase = AddPassengerLogger(AddPassengerUseCase(db), logger)

add_routes_handler = AddRoutesHandler(add_routes_usecase)
availability_handler = RouteAvailabilityHandler(availability_usecase)
view_handler = ViewRoutesHandler(view_usecase)
changeRoutesHandler = ChangeRoutesHandler(edit_routers_usecase, delete_route_usecase)

event_listener = RoutesEventsListener(add_passenger_usecase, config.rabbitmq_url)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(view_handler.router)
app.include_router(availability_handler.router)
app.include_router(add_routes_handler.router)
app.include_router(changeRoutesHandler.router)

event_listener.listen()
