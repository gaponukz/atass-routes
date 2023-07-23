import datetime
import pydantic
from src.business import entities

class GetAviableRoutesDTO(pydantic.BaseModel):
    move_from_city: str
    move_to_city: str
    date: entities.DayDate

class AddRoutesDTO(pydantic.BaseModel):
    route_prototype: entities.RoutePrototype
    departure_dates: list[datetime.datetime]

class UpdateRoutesDTO(pydantic.BaseModel):
    route: entities.Route
