import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.entities import ShortRoute
from src.domain.entities import PathInfo
from src.domain.entities import Route
from src.domain.entities import HashId

class ViewService(typing.Protocol):
    def get_unique_routes(self) -> list[ShortRoute]: ...
    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]: ...
    def get_route_by_id(self, route_id: HashId) -> Route: ...
    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfo: ...

class ViewServiceLogger:
    def __init__(self, service: ViewService, logger: ILogger):
        self._service = service
        self._logger = logger

    def get_unique_routes(self) -> list[ShortRoute]:
        try:
            return self._service.get_unique_routes()
        
        except Exception as error:
            self._logger.error(f"Error retrieving unique routes, got error: {error.__class__.__name__}: {error}")
            raise error            

    def get_routes_family_by_cities(self, move_from_city: str, move_to_city: str) -> list[Route]:
        try:
            return self._service.get_routes_family_by_cities(move_from_city, move_to_city)
        
        except Exception as error:
            self._logger.error(f"Error retrieving routes by cities, got error: {error.__class__.__name__}: {error}")
            raise error

    def get_route_by_id(self, route_id: HashId) -> Route:
        try:
            return self._service.get_route_by_id(route_id)
        
        except Exception as error:
            self._logger.error(f"Error retrieving route by ID ({route_id}), got error: {error.__class__.__name__}: {error}")
            raise error

    def get_path_info(self, route_id: HashId, move_from: HashId, move_to: HashId) -> PathInfo:
        try:
            return self._service.get_path_info(route_id, move_from, move_to)
        
        except Exception as error:
            self._logger.error(f"Error retrieving path info, got error: {error.__class__.__name__}: {error}")
            raise error
