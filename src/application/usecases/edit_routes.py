import typing
from src.domain.value_objects import HashId
from src.domain.entities import Route
from src.application.dto import UpdateRoutesDTO

class UpdateAbleDataBase(typing.Protocol):
    def by_id(self, route_id: HashId) -> Route: ...

    def update(self, route: Route): ...

class EditRoutersUseCase:
    def __init__(self, db: UpdateAbleDataBase):
        self._db = db
    
    def update(self, dto: UpdateRoutesDTO):
        route = self._db.by_id(dto.route.id)
        dto.route.passengers = route.passengers
        
        self._db.update(dto.route)
