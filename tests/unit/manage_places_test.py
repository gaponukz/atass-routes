import datetime
from src.domain.entities import Route
from src.domain.entities import Spot
from src.domain.entities import Place
from src.domain.entities import Passenger
from src.domain.errors import CannotKillPassengersError
from src.domain.errors import RouteNotFoundError
from src.domain.errors import PassengerNotFoundError
from src.domain.errors import PaymentDuplicationError
from src.domain.events import PaymentProcessed
from src.application.dto import DeletePassengerDTO
from src.application.usecases.manage_passengers import ManagePassengersUseCase

class DataBaseMock:
    def __init__(self):
        self.routes = [
            Route(
                id="12345",
                passengers_number=3,
                move_from=Spot(
                    id='start',
                    place=Place(country="Ac", city="Ac", street="As"),
                    date=datetime.datetime.now() + datetime.timedelta(minutes=10),
                ),
                move_to=Spot(
                    id='end',
                    place=Place(country="Bc", city="Bc", street="Bs"),
                    date=datetime.datetime.now() + datetime.timedelta(hours=5),
                ),
                sub_spots=[
                    Spot(
                        id='sub1',
                        place=Place(country="Cc", city="Cc", street="Cs"),
                        date=datetime.datetime.now() + datetime.timedelta(hours=1)
                    ),
                    Spot(
                        id='sub2',
                        place=Place(country="Dc", city="Dc", street="Ds"),
                        date=datetime.datetime.now() + datetime.timedelta(hours=2)
                    ),
                    Spot(
                        id='sub3',
                        place=Place(country="Ec", city="Ec", street="Es"),
                        date=datetime.datetime.now() + datetime.timedelta(hours=3)
                    ),
                ],
                passengers=[
                    Passenger(
                        id="p1",
                        full_name="Af Al",
                        phone_number="1",
                        moving_from_id="start",
                        moving_towards_id="end",
                        gmail="email@example.com",
                    ),
                    Passenger(
                        id="p2",
                        full_name="Bf Bl",
                        phone_number="2",
                        moving_from_id="start",
                        moving_towards_id="sub3",
                        gmail="email@example.com",
                    ),
                ],
                prices={
                    "start": {
                        "end": 5, "sub3": 4, "sub2": 3, "sub1": 2
                    },
                    "sub1": {
                        "end": 4, "sub3": 3, "sub2": 2,
                    },
                    "sub2": {
                        "end": 3, "sub3": 2,
                    },
                    "sub3": {
                        "end": 2
                    }
                },
                description={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                transportation_rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
            )
        ]

    def update(self, route: Route):
        for i in range(len(self.routes)):
            if self.routes[i].id == route.id:
                self.routes[i] = route

    def read_all(self) -> list[Route]:
        return self.routes

def test_add_passenger():
    db = DataBaseMock()
    service = ManagePassengersUseCase(db)

    passenger1 = Passenger(
        id='1',
        full_name="Ada Nab",
        phone_number="123",
        moving_from_id="start",
        moving_towards_id="end",
        gmail="email@example.com",
    )

    try:
        service.add_passenger(PaymentProcessed(payment_id="1", route_id="none_existing_id", passenger=passenger1))
    
    except RouteNotFoundError as e:
        assert e.route_id == "none_existing_id"
    
    else:
        assert False, "Why we can add a passenger to non existent route?"
    
    service.add_passenger(PaymentProcessed(payment_id="2", route_id="12345", passenger=passenger1))

    assert len(db.routes[0].passengers) == 3

    try:
        service.add_passenger(PaymentProcessed(payment_id="2", route_id="none_existing_id", passenger=passenger1))
    
    except PaymentDuplicationError as e:
        assert e.payment_id == "2"
    
    else:
        assert False, "Duplicate!"

    try:
        service.add_passenger(PaymentProcessed(payment_id="3", route_id="12345", passenger=passenger1))
    
    except CannotKillPassengersError as e:
        assert e.passengers_number == 3
    
    else:
        if len(db.routes[0].passengers) == 4:
            assert False, "Why we can add a passenger to full bus?"
        
        else:
            assert False, 'passenger was not added but got "OK"'

def test_delete_passenger():
    db = DataBaseMock()
    service = ManagePassengersUseCase(db)

    try:
        service.delete_passenger(DeletePassengerDTO(route_id="12346", move_from_id="start", move_to_id="sub3", passenger_id="p2"))
    
    except RouteNotFoundError as error:
        assert error.route_id == "12346"
    
    else:
        assert False, "Why we can delete a passenger from non existent route?"
    
    try:
        service.delete_passenger(DeletePassengerDTO(route_id="12345", move_from_id="start", move_to_id="sub3", passenger_id="lol"))

    except PassengerNotFoundError:
        pass

    else:
        assert False, "Why we can delete a non existent passenger?"

    assert len(db.routes[0].passengers) == 2

    service.delete_passenger(DeletePassengerDTO(route_id="12345", move_from_id="start", move_to_id="sub3", passenger_id="p2"))

    assert len(db.routes[0].passengers) == 1
