import typing
from src.infrastructure.logger._interface import ILogger
from src.application.dto import AddPassengerDTO

class AddPassengerService(typing.Protocol):
    def add_passenger(self, data: AddPassengerDTO): ...

class AddPassengerLogger:
    def __init__(self, service: AddPassengerService, logger: ILogger):
        self._service = service
        self._logger = logger

    def add_passenger(self, data: AddPassengerDTO):
        try:
            self._service.add_passenger(data)
            self._logger.info(f"Passenger added: {data}")
        
        except Exception as error:
            self._logger.error(f"Error adding passenger ({data}), got error: {error.__class__.__name__}: {error}")
            raise error
