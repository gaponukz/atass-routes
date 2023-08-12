import typing
from fastapi import APIRouter
from fastapi import HTTPException
from src.domain.entities import Route
from src.domain.entities import HashId
from src.domain.entities import ShortRoute
from src.domain.entities import PathInfo
from src.domain.errors import RouteNotFoundError
from src.domain.errors import SpotNotFoundError

class ViewService(typing.Protocol):
    def get_unique_routes(self) -> list[ShortRoute]: ...

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]: ...

    def get_route_by_id(self, route_id: HashId) -> Route: ...

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfo: ...

class ViewRoutesHandler:
    def __init__(self, service: ViewService):
        self.router = APIRouter()
        self._service = service

        self.router.add_api_route("/get_unique_routes", self.get_unique_routes, methods=["GET"])
        self.router.add_api_route("/get_routes_family", self.get_routes_family_by_cities, methods=["GET"])
        self.router.add_api_route("/get_route_by_id", self.get_route_by_id, methods=["GET"])
        self.router.add_api_route("/get_path_info", self.get_path_info, methods=["GET"])
    
    def get_unique_routes(self) ->  list[ShortRoute]:
        return self._service.get_unique_routes()
    
    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        return self._service.get_routes_family_by_cities(move_from_city, move_to_city)
    
    def get_route_by_id(self, route_id: HashId) -> Route:
        try:
            return self._service.get_route_by_id(route_id)
        
        except RouteNotFoundError:
            raise HTTPException(status_code=404, detail="route not found")

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfo:
        try:
            return self._service.get_path_info(route_id, move_from=move_from, move_to=move_to)
        
        except (RouteNotFoundError, SpotNotFoundError) as error:
            raise HTTPException(status_code=404, detail=str(error))
