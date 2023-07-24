import typing
from src.business.entities import HashId
from src.business.entities import Route
from src.business.entities import Passenger
from src.business.errors import RouteNotFoundError
from src.business.errors import CannotKillPassengersError

class Database(typing.Protocol):
    def read_all(self) -> list[Route]: ...

    def update(self, route: Route): ...

class AddPassangerUseCase:
    def __init__(self, db: Database):
        self._db = db
    
    def add_passanger(self, route_id: HashId, passanger: Passenger):
        routes = list(filter(lambda r: r.id == route_id, self._db.read_all()))

        if not routes:
            raise RouteNotFoundError(route_id)
        
        route = routes[0]
        route.passengers.append(passanger)

        if len(route.passengers) > route.passengers_number:
            raise CannotKillPassengersError(route.passengers_number)

        self._db.update(route)
