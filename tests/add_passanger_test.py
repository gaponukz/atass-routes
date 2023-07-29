import datetime
from src.business.entities import Route
from src.business.entities import Spot
from src.business.entities import Place
from src.business.entities import Passenger
from src.usecases.add_passanger import AddPassangerUseCase
from src.business.errors import CannotKillPassengersError
from src.business.errors import RouteNotFoundError

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
                        first_name="Af",
                        last_name="Al",
                        phone_number="1",
                        moving_from_id="start",
                        moving_towards_id="end",
                    ),
                    Passenger(
                        id="p2",
                        first_name="Bf",
                        last_name="Bl",
                        phone_number="2",
                        moving_from_id="start",
                        moving_towards_id="sub3",
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
                }
            )
        ]

    def update(self, route: Route):
        for i in range(len(self.routes)):
            if self.routes[i].id == route.id:
                self.routes[i] = route

    def read_all(self) -> list[Route]:
        return self.routes

def test_add_passanger():
    db = DataBaseMock()
    service = AddPassangerUseCase(db)

    passenger1 = Passenger(
        first_name="Ada",
        last_name="Nab",
        phone_number="123",
        moving_from_id="start",
        moving_towards_id="end"
    )

    try:
        service.add_passanger("none_existing_id", passenger1)
    
    except RouteNotFoundError as e:
        assert e.route_id == "none_existing_id"
    
    else:
        assert False, "Why we can add a passenger to non existent route?"
    
    service.add_passanger("12345", passenger1)

    assert len(db.routes[0].passengers) == 3

    try:
        service.add_passanger("12345", passenger1)
    
    except CannotKillPassengersError as e:
        assert e.passengers_number == 3
    
    else:
        if len(db.routes[0].passengers) == 4:
            assert False, "Why we can add a passenger to full bus?"
        
        else:
            assert False, 'passanger was not added but got "OK"'
