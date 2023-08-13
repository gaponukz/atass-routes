import typing
from src.infrastructure.logger._interface import ILogger
from src.application.dto import UpdateRoutesDTO

class EditRoutersService(typing.Protocol):
    def update(self, dto: UpdateRoutesDTO): ...

class EditRoutersLogger:
    def __init__(self, service: EditRoutersService, logger: ILogger):
        self._service = service
        self._logger = logger

    def update(self, dto: UpdateRoutesDTO):
        try:
            self._service.update(dto)
            self._logger.info(f"Route updated: {dto}")
        
        except Exception as error:
            self._logger.error(f"Error updating route ({dto}), got error: {error.__class__.__name__}: {error}")
            raise error
