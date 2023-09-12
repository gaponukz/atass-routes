import time
import types
import typing
from src.infrastructure.logger._interface import ILogger

class TimeLoggerConfig(typing.TypedDict):
    info: int
    debug: int
    error: int

_ClassInstance  = typing.TypeVar("_ClassInstance")
_ReturnType = typing.TypeVar("_ReturnType")

class TimeLoggeredDecoratorFactory:
    def __init__(self, logger: ILogger, config: TimeLoggerConfig):
        self._logger = logger
        self._config = config
    
    def _decorate(self, method: typing.Callable[..., _ReturnType], *args, **kwargs) -> _ReturnType:
        start_time = time.monotonic()
        try:
            return method(*args, **kwargs)
        
        finally:
            delta = time.monotonic() - start_time
            
            if isinstance(method, types.MethodType):
                text = f"Time of {method.__self__.__class__.__name__}.{method.__class__.__name__}: {delta}"
            
            else:
                text = f"Time of {method.__class__.__name__}: {delta}"
            
            if 0 <= delta <= self._config['info']:
                self._logger.info(text)
            
            elif self._config['info'] <= delta <= self._config['debug']:
                self._logger.warn(text)
            
            elif delta >= self._config['error']:
                self._logger.error(text)

    def decorate(self, cls: _ClassInstance) -> _ClassInstance:        
        for field in cls.__dict__:
            if field.startswith('_'):
                continue

            if not callable(getattr(cls, field, None)):
                continue

            def __proxy(*args, **kwargs):
                return self._decorate(getattr(cls, field), *args, **kwargs)
            
            setattr(cls, field, __proxy)

        return cls
