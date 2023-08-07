import typing
from src.business.entities import Route
from src.business.entities import HashId
from src.business.entities import ShortRoute
from src.business.entities import PathInfo
from src.business.errors import RouteNotFoundError
from src.business.errors import SpotNotFoundError

class ReadAbleDataBase(typing.Protocol):
    def read_all(self) -> list[Route]: ...

class ViewRoutesUseCase:
    def __init__(self, db: ReadAbleDataBase) -> None:
        self._db = db
    
    def get_unique_routes(self) -> list[ShortRoute]:
        routes = self._db.read_all()
        unique: dict[str, ShortRoute] = {}

        for route in routes:
            key = f"{route.move_from.place.city}-{route.move_to.place.city}"

            if not unique.get(key):
                unique[key] = self._shorten_route(route)
            
            unique[key].count += 1

        return list(unique.values())

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        routes = self._db.read_all()
        filtered = filter(lambda route: route.move_from.place.city.lower() == move_from_city.lower() 
                          and route.move_to.place.city.lower() == move_to_city.lower(), routes)

        return list(filtered)
    
    def get_route_by_id(self, route_id: HashId) -> Route:
        routes = self._db.read_all()
        filtered = list(filter(lambda route: route.id == route_id, routes))

        if not filtered:
            raise RouteNotFoundError(route_id)

        return filtered[0]

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfo:
        route = self.get_route_by_id(route_id)
        routes_spots = route.sub_spots.copy()
        routes_spots.insert(0, route.move_from)
        routes_spots.insert(-1, route.move_to)

        from_spot = list(filter(lambda s: s.id == move_from, routes_spots))
        to_spot = list(filter(lambda s: s.id == move_to, routes_spots))

        if not from_spot:
            raise SpotNotFoundError(route_id, move_from)

        if not to_spot:
            raise SpotNotFoundError(route_id, move_to)
        
        return PathInfo(
            move_from=from_spot[0],
            move_to=to_spot[0],
            price=route.prices[move_from][move_to],
            root_route_id=route_id,
            description=route.description,
            transportation_rules=route.transportation_rules,
            rules=route.rules
        )

    def _shorten_route(self, route: Route) -> ShortRoute:
        return ShortRoute(
            move_from=route.move_from.place.copy(),
            move_to=route.move_to.place.copy(),
            count=0
        )
