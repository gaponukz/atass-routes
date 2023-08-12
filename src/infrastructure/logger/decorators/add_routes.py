import typing
from src.infrastructure.logger._interface import ILogger
from src.application.dto import AddRoutesDTO

class AddRoutesService(typing.Protocol):
    def create_routes_from_prototype(self, dto: AddRoutesDTO): ...

class AddRoutesLogger:
    def __init__(self, service: AddRoutesService, logger: ILogger):
        self._service = service
        self._logger = logger

    def create_routes_from_prototype(self, dto: AddRoutesDTO):
        try:
            self._service.create_routes_from_prototype(dto)
            self._logger.info(f"Routes created from prototype: {dto}")
        
        except Exception as error:
            self._logger.error(f"Error creating routes from prototype ({dto}), got error: {error.__class__.__name__}: {error}")
            raise error
