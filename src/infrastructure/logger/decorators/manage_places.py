import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.events import PaymentProcessed
from src.application.dto import DeletePassengerDTO

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

    def delete_passenger(self, data: DeletePassengerDTO): ...

class PlaceServiceLogger:
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

    def delete_passenger(self, data: DeletePassengerDTO):
        try:
            self._service.delete_passenger(data)
            self._logger.info(f"Passenger deleted: {data}")
        
        except Exception as error:
            self._logger.error(f"Error deleting passenger ({data}), got error: {error.__class__.__name__}: {error}")
            raise error
