import typing
from fastapi import APIRouter
from src.business.entities import Path

class AvailabilityService(typing.Protocol):
    def generate_pathes(self, move_from_city: str, move_to_city: str) -> list[Path]: ...

class RouteAvailabilityHandler:
    def __init__(self, service: AvailabilityService):
        self._service = service
        self.router = APIRouter()

        self.router.add_api_route("/available", self.generate_pathes, methods=["GET"])

    def generate_pathes(self, move_from_city: str, move_to_city: str) -> list[Path]:
        return self._service.generate_pathes(move_from_city, move_to_city)
