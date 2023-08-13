import typing
import datetime
import uuid
from src.domain.entities import Route
from src.domain.value_objects import HashId
from src.domain.value_objects import PricesSchema
from src.application.dto import RoutePrototypeDTO
from src.application.dto import AddRoutesDTO

class CreatAbleDatabase(typing.Protocol):
    def create(self, route: Route): ...

class AddRoutesUseCase:
    def __init__(self, db: CreatAbleDatabase) -> None:
        self._db = db
    
    def create_routes_from_prototype(self, dto: AddRoutesDTO):
        for route in self._generate_copies(dto):
            self._db.create(route)

    def _generate_copies(self, dto: AddRoutesDTO) -> list[Route]:
        routes: list[Route] = []

        for departure_date in dto.departure_dates:
            new_route = self._route_from_prototype(dto.route_prototype.copy(deep=True), departure_date)

            ids_replacements: dict[HashId, HashId] = {}
            new_prices: PricesSchema = {}

            move_from_id = str(uuid.uuid4())
            move_to_id = str(uuid.uuid4())
        
            new_route.move_from.id = move_from_id
            new_route.move_to.id = move_to_id

            ids_replacements[dto.route_prototype.move_from.id] = move_from_id
            ids_replacements[dto.route_prototype.move_to.id] = move_to_id

            for spot in new_route.sub_spots:
                spot_id = str(uuid.uuid4())
                fake_spot_id = spot.id
                ids_replacements[fake_spot_id] = spot_id

                spot.id = spot_id

            for _id in dto.route_prototype.prices:
                new_prices[ids_replacements[_id]] = {}

                for inner_id in dto.route_prototype.prices[_id]:
                    new_prices[ids_replacements[_id]][ids_replacements[inner_id]] = dto.route_prototype.prices[_id][inner_id]
            
            new_route.prices = new_prices
            
            routes.append(new_route)

        return routes
    
    def _route_from_prototype(self, prototype: RoutePrototypeDTO, date: datetime.datetime) -> Route:
        new_route = prototype.copy().dict()
        new_route['move_from']['date'] = date
        new_route['move_to']['date'] = date + datetime.timedelta(minutes=prototype.move_to.from_start)

        for i in range(len(prototype.sub_spots)):
            new_route['sub_spots'][i]['date'] = date + datetime.timedelta(minutes=prototype.sub_spots[i].from_start)
        
        return Route(**new_route)
