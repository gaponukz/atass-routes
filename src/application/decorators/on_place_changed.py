import typing
from src.domain.events import PaymentProcessed
from src.domain.events import PassengerPlaceEvent
from src.application.dto import DeletePassengerDTO

class PlaceService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

    def delete_passenger(self, data: DeletePassengerDTO): ...

class EventSender(typing.Protocol):
    def publish_event(self, event: PassengerPlaceEvent): ...

class SendEventOnPlaceChangedDecorator:
    def __init__(self, base: PlaceService, sender: EventSender):
        self._base = base
        self._sender = sender
    
    def add_passenger(self, event: PaymentProcessed):
        self._base.add_passenger(event)
        
        if not event.passenger.is_anonymous:
            self._sender.publish_event(PassengerPlaceEvent(
                type='booked',
                route_id=event.route_id,
                move_from_id=event.passenger.moving_from_id,
                move_to_id=event.passenger.moving_towards_id,
                passenger_id=event.passenger.id,
            ))

    def delete_passenger(self, data: DeletePassengerDTO):
        self._base.delete_passenger(data)

        self._sender.publish_event(PassengerPlaceEvent(
            type='removed',
            route_id=data.route_id,
            move_from_id=data.move_from_id,
            move_to_id=data.move_to_id,
            passenger_id=data.passenger_id
        ))
