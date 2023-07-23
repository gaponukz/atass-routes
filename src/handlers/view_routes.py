import typing
from fastapi import APIRouter
from fastapi import HTTPException
from src.business.entities import Route
from src.business.entities import HashId
from src.business.entities import ShortRoute
from src.business.entities import PublicRoute
from src.business.errors import RouteNotFoundError

class ViewService(typing.Protocol):
    def get_unique_routes(self) -> list[ShortRoute]: ...

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]: ...

    def get_route_by_id(self, route_id: HashId) -> Route: ...

    def get_route_info(self, route_id: HashId) -> PublicRoute: ...

class ViewRoutesHandler:
    def __init__(self, service: ViewService):
        self.router = APIRouter()
        self._service = service

        self.router.add_api_route("/get_unique_routes", self.get_unique_routes, methods=["GET"])
        self.router.add_api_route("/get_routes_family", self.get_routes_family_by_cities, methods=["POST"])
        self.router.add_api_route("/get_route_by_id", self.get_route_by_id, methods=["GET"])
        self.router.add_api_route("/get_route_info", self.get_route_info, methods=["GET"])
    
    def get_unique_routes(self) ->  list[ShortRoute]:
        return self._service.get_unique_routes()
    
    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        return self._service.get_routes_family_by_cities(move_from_city, move_to_city)
    
    def get_route_by_id(self, route_id: HashId) -> Route:
        try:
            return self._service.get_route_by_id(route_id)
        
        except RouteNotFoundError:
            raise HTTPException(status_code=404, detail="route not found")

    def get_route_info(self, route_id: HashId) -> PublicRoute:
        try:
            return self._service.get_route_info(route_id)
        
        except RouteNotFoundError:
            raise HTTPException(status_code=404, detail="route not found")