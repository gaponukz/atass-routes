import copy
import typing
from src.domain.entities import Route
from src.domain.value_objects import HashId
from src.domain.errors import SpotNotFoundError
from src.application.dto import ShortRouteDTO
from src.application.dto import PathInfoDTO

class ReadAbleDataBase(typing.Protocol):
    def read_all(self) -> list[Route]: ...

    def by_cities(self, move_from: str, move_to: str) -> list[Route]: ...

    def by_id(self, route_id: HashId) -> Route: ...

class ViewRoutesUseCase:
    def __init__(self, db: ReadAbleDataBase) -> None:
        self._db = db
    
    def get_unique_routes(self) -> list[ShortRouteDTO]:
        routes = self._db.read_all()
        unique: dict[str, ShortRouteDTO] = {}

        for route in routes:
            key = f"{route.move_from.place.city}-{route.move_to.place.city}"

            if not unique.get(key):
                unique[key] = self._shorten_route(route)
            
            unique[key].count += 1

        return list(unique.values())

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        return self._db.by_cities(move_from_city, move_to_city)
    
    def get_route_by_id(self, route_id: HashId) -> Route:
        return self._db.by_id(route_id)

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfoDTO:
        route = self._db.by_id(route_id)
        routes_spots = route.sub_spots.copy()
        routes_spots.insert(0, route.move_from)
        routes_spots.insert(-1, route.move_to)

        from_spot = list(filter(lambda s: s.id == move_from, routes_spots))
        to_spot = list(filter(lambda s: s.id == move_to, routes_spots))

        if not from_spot:
            raise SpotNotFoundError(route_id, move_from)

        if not to_spot:
            raise SpotNotFoundError(route_id, move_to)
        
        return PathInfoDTO(
            move_from=from_spot[0],
            move_to=to_spot[0],
            price=route.prices[move_from][move_to],
            root_route_id=route_id,
            description=route.description,
            transportation_rules=route.transportation_rules,
            rules=route.rules
        )

    def _shorten_route(self, route: Route) -> ShortRouteDTO:
        return ShortRouteDTO(
            move_from=copy.deepcopy(route.move_from.place),
            move_to=copy.deepcopy(route.move_to.place),
            count=0
        )
