import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.events import PaymentProcessed

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

class AddPassengerLogger:
    def __init__(self, service: AddPassengerService, logger: ILogger):
        self._service = service
        self._logger = logger

    def add_passenger(self, event: PaymentProcessed):
        try:
            self._service.add_passenger(event)
            self._logger.info(f"Passenger added: {event}")
        
        except Exception as error:
            self._logger.error(f"Error adding passenger ({event}), got error: {error.__class__.__name__}: {error}")
            raise error
