import time
import typing
from src.infrastructure.logger._interface import ILogger
from src.domain.entities import Path
from src.application.dto import GetAviableRoutesDTO

class AvailabilityService(typing.Protocol):
    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]: ...
    def get_availability_graph(self) -> dict[str, list[str]]: ... 

_Method = typing.TypeVar('_Method', bound=typing.Callable)

class AvailabilityTimedLoggeredDecorator:
    def __init__(self, service: AvailabilityService, logger: ILogger):
        self._service = service
        self._logger = logger

    def _log_time(self, method_name, elapsed_time):
        self._logger.info(f"T({self._service.__class__.__name__}.{method_name})={elapsed_time:.4f}")
    
    def _decorate(self, method: _Method) -> _Method:
        def __inner(*args, **kwargs):
            start_time = time.monotonic()
            try:
                return method(*args, **kwargs)
            
            finally:
                elapsed_time = time.monotonic() - start_time
                self._log_time(method.__name__, elapsed_time)
        
        return typing.cast(_Method, __inner)
    
    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]:
        return self._decorate(self._service.generate_pathes)(dto)

    def get_availability_graph(self) -> dict[str, list[str]]:
        return self._decorate(self._service.get_availability_graph)()
