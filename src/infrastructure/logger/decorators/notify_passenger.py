import typing
from src.infrastructure.logger._interface import ILogger
from src.application.dto import NotifyPassengerDTO

class PassengerNotifier(typing.Protocol):
    def notify(self, data: NotifyPassengerDTO): ...

class NotifyPassengerLogger:
    def __init__(self, service: PassengerNotifier, logger: ILogger):
        self._service = service
        self._logger = logger

    def notify(self, data: NotifyPassengerDTO):
        try:
            self._service.notify(data)
        
        except Exception as error:
            self._logger.error(f"Error notifing passenger ({data}), got error: {error.__class__.__name__}: {error}")
