import typing
from fastapi import APIRouter
from fastapi import HTTPException
from src.domain.entities import Route
from src.domain.value_objects import HashId
from src.domain.errors import RouteNotFoundError
from src.domain.errors import SpotNotFoundError
from src.application.dto import ShortRouteDTO
from src.application.dto import PathInfoDTO

class ViewService(typing.Protocol):
    def get_unique_routes(self) -> list[ShortRouteDTO]: ...

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]: ...

    def get_route_by_id(self, route_id: HashId) -> Route: ...

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfoDTO: ...

class ViewRoutesHandler:
    def __init__(self, service: ViewService):
        self.router = APIRouter()
        self._service = service

        self.router.add_api_route("/api/routes/get_unique_routes", self.get_unique_routes, methods=["GET"])
        self.router.add_api_route("/api/routes/get_routes_family", self.get_routes_family_by_cities, methods=["GET"])
        self.router.add_api_route("/api/routes/get_route_by_id", self.get_route_by_id, methods=["GET"])
        self.router.add_api_route("/api/routes/get_path_info", self.get_path_info, methods=["GET"])
    
    def get_unique_routes(self) ->  list[ShortRouteDTO]:
        return self._service.get_unique_routes()
    
    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        return self._service.get_routes_family_by_cities(move_from_city, move_to_city)
    
    def get_route_by_id(self, route_id: HashId) -> Route:
        try:
            return self._service.get_route_by_id(route_id)
        
        except RouteNotFoundError:
            raise HTTPException(status_code=404, detail="route not found")

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfoDTO:
        try:
            return self._service.get_path_info(route_id, move_from=move_from, move_to=move_to)
        
        except (RouteNotFoundError, SpotNotFoundError) as error:
            raise HTTPException(status_code=404, detail=str(error))
