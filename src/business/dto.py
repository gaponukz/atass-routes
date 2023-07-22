import pydantic
from src.business import entities

class AddRoutesDTO(pydantic.BaseModel):
    route_prototype: entities.RoutePrototype
    datetimes: list[entities.DatetimeObject]

class UpdateRoutesDTO(pydantic.BaseModel):
    route: entities.Route
