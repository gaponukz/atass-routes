import datetime
from src.domain.entities import Route
from src.domain.entities import Place
from src.domain.entities import Spot
from src.domain.entities import Passenger
from src.application.dto import GetAviableRoutesDTO
from src.application.usecases.route_availability import RouteAvailabilityUseCase

class DataBaseStub:
    def with_cities(self, move_from: str, move_to) -> list[Route]:
        return self.read_all()

    def read_all(self) -> list[Route]:
        return [
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
                        id="p3",
                        full_name="Cf Cl",
                        phone_number="3",
                        moving_from_id="sub1",
                        moving_towards_id="sub2",
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

def test_generate_all_pathes():
    service = RouteAvailabilityUseCase(DataBaseStub())
    pathes = service.generate_pathes(GetAviableRoutesDTO(
        move_from_city="Gc",
        move_to_city="Bc",
        date=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    ))

    assert len(pathes) == 0

    pathes = service.generate_pathes(GetAviableRoutesDTO(
        move_from_city="Gc",
        move_to_city="Bc",
        date=datetime.datetime.now().strftime("%d.%m.%Y")
    ))

    assert len(pathes) == 0

    pathes = service.generate_pathes(GetAviableRoutesDTO(
        move_from_city="Ac",
        move_to_city="Bc",
        date=datetime.datetime.now().strftime("%d.%m.%Y")
    ))

    assert len(pathes) == 1

    path = pathes[0]

    assert path.root_route_id == "12345"

    assert path.move_from.id == "start"
    assert path.move_to.id == "end"
    assert path.price == 5

def test_get_availability_graph():
    service = RouteAvailabilityUseCase(DataBaseStub())
    availability_graph = service.get_availability_graph()
    expected_graph = {'Ac': ['Cc', 'Dc', 'Ec', 'Bc'], 'Cc': ['Dc', 'Ec', 'Bc'], 'Dc': ['Ec', 'Bc'], 'Ec': ['Bc']}

    assert availability_graph == expected_graph
