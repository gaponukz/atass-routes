import datetime
from src.domain.entities import Route
from src.domain.entities import Spot
from src.domain.entities import Place
from src.domain.value_objects import HashId
from src.domain.errors import SpotNotFoundError, RouteNotFoundError
from src.application.usecases.view_routes import ViewRoutesUseCase

class DataBaseStub:
    def __init__(self):
        self.routes = [
            Route(
                id="1",
                passengers_number=1,
                move_from=Spot(
                    id="11",
                    place=Place(country="Ac", city="Ac", street="As"),
                    date=datetime.datetime.now()
                ),
                move_to=Spot(
                    id="12",
                    place=Place(country="Bc", city="Bc", street="Bs"),
                    date=datetime.datetime.now()
                ),
                sub_spots=[
                    Spot(
                        id="13",
                        place=Place(country="Cc", city="Cc", street="Cs"),
                        date=datetime.datetime.now()
                    )
                ],
                description={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                transportation_rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                prices={"11": {"12": 100}}
            ),
            Route(
                id="2",
                passengers_number=1,
                move_from=Spot(
                    place=Place(country="Ac", city="Ac", street="As"),
                    date=datetime.datetime.now()
                ),
                move_to=Spot(
                    place=Place(country="Bc", city="Bc", street="Bs"),
                    date=datetime.datetime.now()
                ),
                description={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                transportation_rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
            ),
            Route(
                id="3",
                passengers_number=1,
                move_from=Spot(
                    place=Place(country="Cc", city="Cc", street="Cs"),
                    date=datetime.datetime.now()
                ),
                move_to=Spot(
                    place=Place(country="Dc", city="Dc", street="Ds"),
                    date=datetime.datetime.now()
                ),
                description={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
                transportation_rules={"ua": "Hi", "en": "Hi", "pl": "Hi"},
            )
        ]

    def read_all(self) -> list[Route]:
        return self.routes

    def by_cities(self, move_from: str, move_to: str) -> list[Route]:
        filtered = filter(lambda route: route.move_from.place.city.lower() == move_from.lower() 
                          and route.move_to.place.city.lower() == move_to.lower(), self.routes)

        return list(filtered)

    def by_id(self, route_id: HashId) -> Route:
        filtered = list(filter(lambda route: route.id == route_id, self.routes))

        if not filtered:
            raise RouteNotFoundError(route_id)

        return filtered[0]

def test_get_unique_routes():
    service = ViewRoutesUseCase(DataBaseStub())
    routes = service.get_unique_routes()
    assert len(routes) == 2

    short_route = list(filter(lambda x: x.move_from.city == 'Ac', routes))[0]
    assert short_route.count == 2

    short_route = list(filter(lambda x: x.move_from.city == 'Cc', routes))[0]
    assert short_route.count == 1

def test_get_routes_family_by_cities():
    service = ViewRoutesUseCase(DataBaseStub())
    routes = service.get_routes_family_by_cities("Ac", "Bc")
    assert len(routes) == 2

    routes = service.get_routes_family_by_cities("Cc", "Dc")
    assert len(routes) == 1

def test_get_route_by_id():
    service = ViewRoutesUseCase(DataBaseStub())

    route = service.get_route_by_id("1")
    assert route.id == "1"
    assert route.move_from.place.city == "Ac"

    route = service.get_route_by_id("3")
    assert route.id == "3"
    assert route.move_from.place.city == "Cc"

def test_get_path_info():
    service = ViewRoutesUseCase(DataBaseStub())

    try:
        path = service.get_path_info("1", "14", "12")
    
    except SpotNotFoundError:
        pass
    
    else:
        assert False, "Can find not existing spot"
    
    path = service.get_path_info("1", "11", "12")

    assert path.price == 100
    assert path.description["ua"] == "Hi"
    assert path.root_route_id == "1"
