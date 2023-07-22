import datetime
from src.business.entities import Route
from src.business.entities import Spot
from src.business.entities import Place
from src.business.entities import HashId
from src.usecases.delete_route import DeleteRouteUseCase

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
                sub_spots=[],
                passengers=[],
                prices={}
            )
        ]

    def delete(self, route_id: HashId):
        self.routes = list(filter(lambda x: x.id != route_id, self.routes))

def test_delete():
    db = DataBaseMock()
    service = DeleteRouteUseCase(db)

    service.delete("12345")

    assert len(db.routes) == 0
