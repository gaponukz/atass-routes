import typing
from src.domain.entities import Route
from src.domain.entities import Spot
from src.domain.value_objects import HashId
from src.domain.events import PassengerPlaceEvent
from src.domain.errors import RouteNotFoundError

class Database(typing.Protocol):
    def read_all(self) -> list[Route]: ...

class DeleteRouteService(typing.Protocol):
    def delete(self, route_id: HashId): ...

class EventSender(typing.Protocol):
    def publish_event(self, event: PassengerPlaceEvent): ...

class SendEventOnDeleteRouteDecorator:
    def __init__(self, base: DeleteRouteService, sender: EventSender, db: Database):
        self._base = base
        self._sender = sender
        self._db = db
    
    def delete(self, route_id: HashId):
        routes = self._db.read_all()
        routes = list(filter(lambda route: route.id == route_id, routes))

        if not routes:
            raise RouteNotFoundError(route_id)
        
        try:
            route = routes[0]

            for passenger in route.passengers:
                self._sender.publish_event(PassengerPlaceEvent(
                    type='removed',
                    route_id=route.id,
                    move_from_id=passenger.moving_from_id,
                    move_to_id=passenger.moving_towards_id,
                    passenger_id=passenger.id
                ))
        
        finally:
            self._base.delete(route_id)
