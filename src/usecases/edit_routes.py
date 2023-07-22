import typing
from src.business.entities import Route
from src.business.dto import UpdateRoutesDTO

class UpdateAbleDataBase(typing.Protocol):
    def update(self, route: Route): ...

class EditRoutersUseCase:
    def __init__(self, db: UpdateAbleDataBase):
        self._db = db
    
    def update(self, dto: UpdateRoutesDTO):
        self._db.update(dto.route)
