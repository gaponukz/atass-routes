from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infrastructure.settings import settings
from src.infrastructure.db.mongodb import RouteRepository
from src.infrastructure.logger.file import FileWriter
from src.infrastructure.notifier.gmail import GmailNotifier, Creds, Letter
from src.infrastructure.notifier.rabbitmq import RabbitMQEventNotifier

from src.application.usecases.view_routes import ViewRoutesUseCase
from src.application.usecases.route_availability import RouteAvailabilityUseCase
from src.application.usecases.add_routes import AddRoutesUseCase
from src.application.usecases.edit_routes import EditRoutersUseCase
from src.application.usecases.delete_route import DeleteRouteUseCase
from src.application.usecases.manage_passengers import ManagePassengersUseCase
from src.application.decorators.on_place_changed import SendEventOnPlaceChangedDecorator
from src.application.decorators.on_remove_route import SendEventOnDeleteRouteDecorator

from src.infrastructure.handlers.update_route import UpdateRouteHandler
from src.infrastructure.handlers.remove_route import RemoveRouteHandler
from src.infrastructure.handlers.add_routes import AddRoutesHandler
from src.infrastructure.handlers.route_availability import RouteAvailabilityHandler
from src.infrastructure.handlers.view_routes import ViewRoutesHandler
from src.infrastructure.handlers.add_passenger import ChangePlacesHandler

from src.infrastructure.logger.decorators.manage_places import PlaceServiceLogger
from src.infrastructure.logger.decorators.add_routes import AddRoutesLogger
from src.infrastructure.logger.decorators.delete_route import DeleteRouteLogger
from src.infrastructure.logger.decorators.edit_route import EditRoutersLogger
from src.infrastructure.logger.decorators.route_availability import AvailabilityServiceLogger
from src.infrastructure.logger.decorators.view_routes import ViewServiceLogger
from src.infrastructure.logger.decorators.notify_passenger import NotifyPassengerLogger
from src.infrastructure.logger.decorators.publish_event import LogEventSenderDecorator
from src.infrastructure.logger.decorators.db_speed import RepositoryTimedLoggeredDecorator
from src.infrastructure.logger.decorators.availability_speed import AvailabilityTimedLoggeredDecorator

logger = FileWriter("routes_app.log")
timer_logger = FileWriter("routes_app_timing.log")
config = settings.EnvSettingsExporter().load()
db = RepositoryTimedLoggeredDecorator(RouteRepository(config.mongodb_url, "Cluster0"), timer_logger)
event_notifier = LogEventSenderDecorator(RabbitMQEventNotifier(config.rabbitmq_url), logger)
gmail_notifier = NotifyPassengerLogger(GmailNotifier(
    Creds(config.gmail, config.gmail_password),
    Letter("Автобусний Квиток", "letters/new_route.html")
), logger)

view_usecase = ViewServiceLogger(ViewRoutesUseCase(db), logger)
availability_usecase = AvailabilityServiceLogger(AvailabilityTimedLoggeredDecorator(RouteAvailabilityUseCase(db), timer_logger), logger)
add_routes_usecase = AddRoutesLogger(AddRoutesUseCase(db), logger)
edit_routers_usecase = EditRoutersLogger(EditRoutersUseCase(db), logger)
delete_route_usecase = DeleteRouteLogger(SendEventOnDeleteRouteDecorator(DeleteRouteUseCase(db), event_notifier, db), logger)
change_places_usecase = PlaceServiceLogger(SendEventOnPlaceChangedDecorator(ManagePassengersUseCase(db), event_notifier), logger)

add_routes_handler = AddRoutesHandler(add_routes_usecase)
availability_handler = RouteAvailabilityHandler(availability_usecase)
view_handler = ViewRoutesHandler(view_usecase)
update_handler = UpdateRouteHandler(edit_routers_usecase)
delete_handler = RemoveRouteHandler(delete_route_usecase)
add_passenger_handler = ChangePlacesHandler(change_places_usecase, gmail_notifier)

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
app.include_router(update_handler.router)
app.include_router(delete_handler.router)
app.include_router(add_passenger_handler.router)
