from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.settings import settings
from src.infrastructure.db.json_db import RouteRepository
from src.infrastructure.logger.console import ConsoleLogger
from src.infrastructure.notifier.gmail import GmailNotifier, Creds, Letter

from src.application.usecases.view_routes import ViewRoutesUseCase
from src.application.usecases.route_availability import RouteAvailabilityUseCase
from src.application.usecases.add_routes import AddRoutesUseCase
from src.application.usecases.edit_routes import EditRoutersUseCase
from src.application.usecases.delete_route import DeleteRouteUseCase
from src.application.usecases.add_passenger import AddPassengerUseCase

from src.infrastructure.handlers.change_routes import ChangeRoutesHandler
from src.infrastructure.handlers.add_routes import AddRoutesHandler
from src.infrastructure.handlers.route_availability import RouteAvailabilityHandler
from src.infrastructure.handlers.view_routes import ViewRoutesHandler
from src.infrastructure.handlers.add_passenger import RoutesEventsListener

from src.infrastructure.logger.decorators.add_passenger import AddPassengerLogger
from src.infrastructure.logger.decorators.add_routes import AddRoutesLogger
from src.infrastructure.logger.decorators.delete_route import DeleteRouteLogger
from src.infrastructure.logger.decorators.edit_route import EditRoutersLogger
from src.infrastructure.logger.decorators.route_availability import AvailabilityServiceLogger
from src.infrastructure.logger.decorators.view_routes import ViewServiceLogger
from src.infrastructure.logger.decorators.notify_passenger import NotifyPassengerLogger

logger = ConsoleLogger()
db = RouteRepository("routes.json")
config = settings.EnvSettingsExporter().load()
gmail_notifier = NotifyPassengerLogger(GmailNotifier(
    Creds(config.gmail, config.gmail_password),
    Letter("Автобусний Квиток", "letters/new_route.html")
), logger)


view_usecase = ViewServiceLogger(ViewRoutesUseCase(db), logger)
availability_usecase = AvailabilityServiceLogger(RouteAvailabilityUseCase(db), logger)
add_routes_usecase = AddRoutesLogger(AddRoutesUseCase(db), logger)
edit_routers_usecase = EditRoutersLogger(EditRoutersUseCase(db), logger)
delete_route_usecase = DeleteRouteLogger(DeleteRouteUseCase(db), logger)
add_passenger_usecase = AddPassengerLogger(AddPassengerUseCase(db), logger)

add_routes_handler = AddRoutesHandler(add_routes_usecase)
availability_handler = RouteAvailabilityHandler(availability_usecase)
view_handler = ViewRoutesHandler(view_usecase)
changeRoutesHandler = ChangeRoutesHandler(edit_routers_usecase, delete_route_usecase)

try:
    RoutesEventsListener(add_passenger_usecase, gmail_notifier, config.rabbitmq_url).listen()

except Exception as error:
    print("RoutesEventsListener not started")

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
