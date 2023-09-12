import time
import typing
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.infrastructure.logger._interface import ILogger

class RouteRepository(typing.Protocol):
    def create(self, route: Route): ...

    def read_all(self) -> list[Route]: ...

    def by_cities(self, move_from: str, move_to: str) -> list[Route]: ...
    
    def with_cities(self, move_from: str, move_to: str) -> list[Route]: ...

    def by_id(self, route_id: HashId) -> Route: ...

    def update(self, route: Route): ...

    def delete(self, route_id: HashId): ...

_Method = typing.TypeVar('_Method', bound=typing.Callable)

class RepositoryTimedLoggeredDecorator(RouteRepository):
    def __init__(self, base: RouteRepository, logger: ILogger):
        self._base = base
        self._logger = logger

    def _log_time(self, method_name, elapsed_time):
        self._logger.info(f"T({self._base.__class__.__name__}.{method_name})={elapsed_time:.4f}")
    
    def _decorate(self, method: _Method) -> _Method:
        def __inner(*args, **kwargs):
            start_time = time.monotonic()
            try:
                return method(*args, **kwargs)
            
            finally:
                elapsed_time = time.monotonic() - start_time
                self._log_time(method.__name__, elapsed_time)
        
        return typing.cast(_Method, __inner)

    def create(self, route: Route):
        self._decorate(self._base.create)(route)

    def read_all(self) -> list[Route]:
        return self._decorate(self._base.read_all)()

    def by_cities(self, move_from: str, move_to: str) -> list[Route]:
        return self._decorate(self._base.by_cities)(move_from, move_to)

    def with_cities(self, move_from: str, move_to: str) -> list[Route]:
        return self._decorate(self._base.with_cities)(move_from, move_to)

    def by_id(self, route_id: HashId) -> Route:
        return self._decorate(self._base.by_id)(route_id)

    def update(self, route: Route):
        self._decorate(self._base.update)(route)

    def delete(self, route_id: HashId):
        self._decorate(self._base.delete)(route_id)
