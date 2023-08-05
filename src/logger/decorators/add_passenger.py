import typing
from src.logger._interface import ILogger

class AddPassengerService(typing.Protocol):
    def process_message(self, message: str): ...

    def listen(self): ...

class AddPassengerLogger:
    def __init__(self, service: AddPassengerService, logger: ILogger):
        self._service = service
        self._logger = logger

    def process_message(self, message: str):
        try:
            self._service.process_message(message)
            self._logger.info(f"Message ({message}) was processed")
        
        except Exception as error:
            self._logger.error(f"Error processing message ({message}), got error: {error.__class__.__name__}: {error}")

    def listen(self):
        try:
            self._service.listen()
        
        except Exception as error:
            self._logger.error(f"Error on AddPassengerService.listen, got error: {error.__class__.__name__}: {error}")
