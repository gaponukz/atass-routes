import typing
from fastapi import APIRouter
from src.domain.entities import HashId
from src.application.dto import UpdateRoutesDTO

class DeleteRouteService(typing.Protocol):
    def delete(self, route_id: HashId): ...

class EditRoutersService(typing.Protocol):
    def update(self, dto: UpdateRoutesDTO): ...


class ChangeRoutesHandler:
    def __init__(
            self,
            update_service: EditRoutersService,
            delete_service: DeleteRouteService
    ):
        self._update_service = update_service
        self._delete_service = delete_service
        self.router = APIRouter()

        self.router.add_api_route("/routes", self.update, methods=["UPDATE"])
        self.router.add_api_route("/routes", self.detete, methods=["DELETE"])

    def update(self, dto: UpdateRoutesDTO):
        self._update_service.update(dto)
    
    def detete(self, route_id: HashId):
        self._delete_service.delete(route_id)
