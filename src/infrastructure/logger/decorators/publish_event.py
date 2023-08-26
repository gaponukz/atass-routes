import typing
from src.domain.events import PassengerPlaceEvent
from src.infrastructure.logger._interface import ILogger

class EventSender(typing.Protocol):
    def publish_event(self, event: PassengerPlaceEvent): ...

class LogEventSenderDecorator:
    def __init__(self, base: EventSender, logger: ILogger):
        self._base = base
        self._logger = logger
    
    def publish_event(self, event: PassengerPlaceEvent):
        try:
            self._base.publish_event(event)
            self._logger.info(f"Event {event} published")        
        
        except Exception as error:
            self._logger.error(f"Can not publish event {event}, {error.__class__.__name__}: {error}")
