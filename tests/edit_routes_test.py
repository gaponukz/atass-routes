import datetime
from src.domain.entities import Route
from src.domain.entities import Spot
from src.domain.entities import Place
from src.domain.entities import Passenger
from src.application.dto import UpdateRoutesDTO
from src.application.usecases.edit_routes import EditRoutersUseCase

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
                        email_address="email@example.com",
                    ),
                    Passenger(
                        id="p2",
                        full_name="Bf Bl",
                        phone_number="2",
                        moving_from_id="start",
                        moving_towards_id="sub3",
                        email_address="email@example.com",
                    ),
                    Passenger(
                        id="p3",
                        full_name="Cf Cl",
                        phone_number="3",
                        moving_from_id="sub1",
                        moving_towards_id="sub2",
                        email_address="email@example.com",
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

def test_update():
    db = DataBaseMock()
    service = EditRoutersUseCase(db)

    service.update(UpdateRoutesDTO(
        route=Route(
                id="12345",
                passengers_number=5,
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
                        email_address="email@example.com",
                    ),
                    Passenger(
                        id="p2",
                        full_name="Bf Bl",
                        phone_number="2",
                        moving_from_id="start",
                        moving_towards_id="sub3",
                        email_address="email@example.com",
                    )
                ],
                prices={
                    "start": {
                        "end": 5, "sub3": 4, "sub2": 3, "sub1": 2
                    },
                    "sub1": {
                        "end": 4, "sub3": 3, "sub2": 2,
                    },
                    "sub2": {
                        "end": 0, "sub3": 0
                    },
                    "sub3": {
                        "end": 0
                    }
                }
            )
    ))

    new_route = db.routes[0]

    assert new_route.id == "12345"
    assert new_route.passengers_number == 5
    assert new_route.prices['sub2']['end'] == 0
    assert new_route.prices['sub2']['sub3'] == 0
    assert new_route.prices['sub3']['end'] == 0
    assert len(new_route.passengers) == 2
