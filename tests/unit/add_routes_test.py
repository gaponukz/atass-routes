import datetime
from src.domain.entities import Route
from src.domain.entities import Place
from src.application.dto import SpotTemplateDTO
from src.application.dto import SubSpotTemplateDTO
from src.application.dto import RoutePrototypeDTO
from src.application.dto import AddRoutesDTO
from src.application.usecases.add_routes import AddRoutesUseCase

class DataBaseMock:
    def __init__(self) -> None:
        self.routes: list[Route] = []
    
    def create(self, route: Route):
        self.routes.append(route)

now_date = datetime.datetime.now()

prototype = RoutePrototypeDTO(
    passengers_number=5,
    move_from=SpotTemplateDTO(
        id="start",
        place=Place(
            country="Ac",
            city="Ac",
            street="As"
        ),
    ),
    move_to=SpotTemplateDTO(
        id="end",
        place=Place(
            country="Bc",
            city="Bc",
            street="Bs"
        )
    ),
    description={"ua": "Hi", "en": "Hi", "pl": "Hi"},
    rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
    transportation_rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
    sub_spots=[
        SubSpotTemplateDTO(
            id="sub1",
            place=Place(
                country="Cc",
                city="Cc",
                street="Cs"
            ),
            from_start=1500
        )
    ],
    prices={
        "start": {
            "sub1": 5,
            "end": 10
        },
        "sub1": {
            "end": 5
        }
    }
)

def create_routes_from_prototype_test():
    db = DataBaseMock()
    service = AddRoutesUseCase(db)

    service.create_routes_from_prototype(AddRoutesDTO(route_prototype=prototype, departure_dates=[
        (now_date + datetime.timedelta(days=1, hours=4), now_date + datetime.timedelta(days=2, hours=4)),
        (now_date + datetime.timedelta(days=2), now_date + datetime.timedelta(days=3))
    ]))
    
    assert len(db.routes) == 2

    for route in db.routes:
        assert route.move_from.place.city == "Ac"
        assert route.move_to.place.city == "Bc"

        assert route.prices[route.move_from.id][route.move_to.id] == 10
        assert route.move_to.date in [
            now_date + datetime.timedelta(days=2, hours=4),
            now_date + datetime.timedelta(days=3)
            ]
