import typing
from fastapi import APIRouter
from src.domain.value_objects import HashId
from src.application.dto import UpdateRoutesDTO

class EditRoutersService(typing.Protocol):
    def update(self, dto: UpdateRoutesDTO): ...


class UpdateRouteHandler:
    def __init__(self, update_service: EditRoutersService):
        self._update_service = update_service
        self.router = APIRouter()

        self.router.add_api_route("/route", self.update, methods=["PUT"])

    def update(self, dto: UpdateRoutesDTO):
        self._update_service.update(dto)
