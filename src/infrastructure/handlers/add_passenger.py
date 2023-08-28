import typing
import dataclass_factory
from fastapi import APIRouter, Request

from src.domain.events import PaymentProcessed
from src.application.dto import NotifyPassengerDTO

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

class PassengerNotifier(typing.Protocol):
    def notify(self, data: NotifyPassengerDTO): ...

class AddPassengerHandler:
    def __init__(
            self,
            add_passenger_service: AddPassengerService,
            notify_passenger_service: PassengerNotifier
        ):
        
        self.router = APIRouter()
        self.add_passenger_service = add_passenger_service
        self.notify_passenger_service = notify_passenger_service
        self.factory = dataclass_factory.Factory(default_schema=dataclass_factory.Schema(
            name_style=dataclass_factory.NameStyle.camel_lower
        ))

        self.router.add_api_route("/api/routes/add_passenger", self.add_passenger, methods=["POST"])
    
    async def add_passenger(self, request: Request):
        data = self.factory.load(await request.json(), PaymentProcessed)

        self.add_passenger_service.add_passenger(PaymentProcessed(
            route_id=data.route_id,
            passenger=data.passenger
        ))

        self.notify_passenger_service.notify(NotifyPassengerDTO(
            payment_id=data.payment_id,
            passenger=data.passenger
        ))
