import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.value_objects import HashId

class DeleteRouteService(typing.Protocol):
    def delete(self, route_id: HashId): ...

class DeleteRouteLogger:
    def __init__(self, service: DeleteRouteService, logger: ILogger):
        self._service = service
        self._logger = logger

    def delete(self, route_id: HashId):
        try:
            self._service.delete(route_id)
            self._logger.info(f"Route deleted with ID: {route_id}")
        
        except Exception as error:
            self._logger.error(f"Error deleting route with ID ({route_id}), got error: {error.__class__.__name__}: {error}")
            raise error
