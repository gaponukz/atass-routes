import typing
import dataclass_factory
from fastapi import APIRouter, Request

from src.domain.events import PaymentProcessed
from src.application.dto import NotifyPassengerDTO
from src.application.dto import DeletePassengerDTO

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

    def delete_passenger(self, data: DeletePassengerDTO): ...

class PassengerNotifier(typing.Protocol):
    def notify(self, data: NotifyPassengerDTO): ...

class ChangePlacesHandler:
    def __init__(
            self,
            passenger_service: AddPassengerService,
            notify_passenger_service: PassengerNotifier
        ):
        
        self.router = APIRouter()
        self.passenger_service = passenger_service
        self.notify_passenger_service = notify_passenger_service
        self.factory = dataclass_factory.Factory(default_schema=dataclass_factory.Schema(
            name_style=dataclass_factory.NameStyle.camel_lower
        ))

        self.router.add_api_route("/api/routes/add_passenger", self.add_passenger, methods=["POST"])
        self.router.add_api_route("/api/routes/passenger", self.delete_passenger, methods=["DELETE"])
    
    async def add_passenger(self, request: Request):
        data = self.factory.load(await request.json(), PaymentProcessed)

        self.passenger_service.add_passenger(data)

        self.notify_passenger_service.notify(NotifyPassengerDTO(
            payment_id=data.payment_id,
            passenger=data.passenger
        ))

    async def delete_passenger(self, data: DeletePassengerDTO):
        self.passenger_service.delete_passenger(data)
