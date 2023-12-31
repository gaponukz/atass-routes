import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.entities import Path
from src.application.dto import GetAviableRoutesDTO

class AvailabilityService(typing.Protocol):
    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]: ...
    def get_availability_graph(self) -> dict[str, list[str]]: ... 

class AvailabilityServiceLogger:
    def __init__(self, service: AvailabilityService, logger: ILogger):
        self._service = service
        self._logger = logger

    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]:
        try:
            return self._service.generate_pathes(dto)
        
        except Exception as error:
            self._logger.error(f"Error generating paths ({dto}), got error: {error.__class__.__name__}: {error}")
            raise error

    def get_availability_graph(self) -> dict[str, list[str]]:
        try:
            return self._service.get_availability_graph()
        
        except Exception as error:
            self._logger.error(f"Error retrieving availability graph, got error: {error.__class__.__name__}: {error}")
            raise error
