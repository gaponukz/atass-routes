import typing
from src.domain.events import PaymentProcessed
from src.domain.events import PassengerPlaceEvent

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

class EventSender(typing.Protocol):
    def publish_event(self, event: PassengerPlaceEvent): ...

class SendEventOnPassengerAddedDecorator:
    def __init__(self, base: AddPassengerService, sender: EventSender):
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
