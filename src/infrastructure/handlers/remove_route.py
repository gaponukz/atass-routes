import typing
from fastapi import APIRouter
from src.domain.value_objects import HashId
from src.application.dto import UpdateRoutesDTO

class DeleteRouteService(typing.Protocol):
    def delete(self, route_id: HashId): ...


class RemoveRouteHandler:
    def __init__(self, delete_service: DeleteRouteService):
        self._delete_service = delete_service
        self.router = APIRouter()

        self.router.add_api_route("/api/routes/route", self.detete, methods=["DELETE"])
    
    def detete(self, route_id: HashId):
        self._delete_service.delete(route_id)
