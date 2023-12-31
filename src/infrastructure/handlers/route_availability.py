import typing
from fastapi import APIRouter
from src.domain.entities import Path
from src.domain.value_objects import DayDate
from src.application.dto import GetAviableRoutesDTO

class AvailabilityService(typing.Protocol):
    def generate_pathes(self, dto: GetAviableRoutesDTO) -> list[Path]: ...

    def get_availability_graph(self) -> dict[str, list[str]]: ... 

class RouteAvailabilityHandler:
    def __init__(self, service: AvailabilityService):
        self._service = service
        self.router = APIRouter()

        self.router.add_api_route("/api/routes/available", self.generate_pathes, methods=["GET"])
        self.router.add_api_route("/api/routes/availability_graph", self.get_availability_graph, methods=["GET"])
    
    def get_availability_graph(self) -> dict[str, list[str]]:
        return self._service.get_availability_graph()

    def generate_pathes(self, move_from_city: str, move_to_city: str, date: DayDate) -> list[Path]:
        return self._service.generate_pathes(GetAviableRoutesDTO(
            move_from_city=move_from_city,
            move_to_city=move_to_city,
            date=date
        ))
