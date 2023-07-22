import typing
from fastapi import APIRouter
from src.business.entities import Path

class AvailabilityService(typing.Protocol):
    def generate_all_pathes(self) -> list[Path]: ...

class RouteAvailabilityHandler:
    def __init__(self, service: AvailabilityService):
        self._service = service
        self.router = APIRouter()

        self.router.add_api_route("/available", self.generate_all_pathes, methods=["GET"])

    def generate_all_pathes(self) -> list[Path]:
        return self._service.generate_all_pathes()
