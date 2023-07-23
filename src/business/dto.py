import datetime
import pydantic
from src.business import entities

class AddRoutesDTO(pydantic.BaseModel):
    route_prototype: entities.RoutePrototype
    departure_dates: list[datetime.datetime]

class UpdateRoutesDTO(pydantic.BaseModel):
    route: entities.Route
