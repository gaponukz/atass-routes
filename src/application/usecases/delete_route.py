import typing
from src.domain.entities import HashId

class DeleteAbleDataBase(typing.Protocol):
    def delete(self, route_id: HashId): ...

class DeleteRouteUseCase:
    def __init__(self, db: DeleteAbleDataBase):
        self._db = db
    
    def delete(self, route_id: HashId):
        self._db.delete(route_id)
