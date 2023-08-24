import typing
from fastapi import APIRouter
from src.application.dto import AddRoutesDTO

class AddRoutesService(typing.Protocol):
    def create_routes_from_prototype(self, dto: AddRoutesDTO): ...

class AddRoutesHandler:
    def __init__(self, sevice: AddRoutesService):
        self._sevice = sevice
        self.router = APIRouter()

        self.router.add_api_route("/api/routes/add_routes", self.add_routes, methods=["POST"])
    
    def add_routes(self, dto: AddRoutesDTO):
        self._sevice.create_routes_from_prototype(dto)
