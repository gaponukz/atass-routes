import typing
from src.domain.entities import Route
from src.domain.events import PaymentProcessed
from src.domain.errors import RouteNotFoundError
from src.domain.errors import CannotKillPassengersError

class Database(typing.Protocol):
    def read_all(self) -> list[Route]: ...

    def update(self, route: Route): ...

class AddPassengerUseCase:
    def __init__(self, db: Database):
        self._db = db
    
    def add_passenger(self, event: PaymentProcessed):
        routes = list(filter(lambda r: r.id == event.route_id, self._db.read_all()))

        if not routes:
            raise RouteNotFoundError(event.route_id)
        
        route = routes[0]
        route.passengers.append(event.passenger)

        if len(route.passengers) > route.passengers_number:
            raise CannotKillPassengersError(route.passengers_number)

        self._db.update(route)
