import typing
from src.domain.entities import Route
from src.domain.events import PaymentProcessed
from src.domain.errors import RouteNotFoundError
from src.domain.errors import CannotKillPassengersError
from src.domain.errors import PaymentDuplicationError
from src.domain.errors import PassengerNotFoundError
from src.application.dto import DeletePassengerDTO

class Database(typing.Protocol):
    def read_all(self) -> list[Route]: ...

    def update(self, route: Route): ...

class ManagePassengersUseCase:
    def __init__(self, db: Database, last_payment_number: int = 100):
        self._db = db
        self._last_payment_number = last_payment_number
        self._last_payments: set[str] = set()
    
    def add_passenger(self, event: PaymentProcessed):
        if event.payment_id in self._last_payments:
            raise PaymentDuplicationError(event.payment_id)

        routes = list(filter(lambda r: r.id == event.route_id, self._db.read_all()))

        if not routes:
            raise RouteNotFoundError(event.route_id)
        
        route = routes[0]
        route.passengers.append(event.passenger)

        if len(route.passengers) > route.passengers_number:
            raise CannotKillPassengersError(route.passengers_number)

        self._last_payments.add(event.payment_id)

        if len(self._last_payments) == self._last_payment_number:
            self._last_payments.pop()
        
        self._db.update(route)
    
    def delete_passenger(self, data: DeletePassengerDTO):
        routes = list(filter(lambda r: r.id == data.route_id, self._db.read_all()))

        if not routes:
            raise RouteNotFoundError(data.route_id)
        
        route = routes[0]
        before = len(route.passengers)

        route.passengers = [passenger for passenger in route.passengers if passenger.id != data.passenger_id]

        if before == len(route.passengers):
            raise PassengerNotFoundError()

        self._db.update(route)
