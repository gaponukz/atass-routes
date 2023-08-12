import datetime
import pydantic
from src.domain import entities

class GetAviableRoutesDTO(pydantic.BaseModel):
    move_from_city: str
    move_to_city: str
    date: entities.DayDate

class AddRoutesDTO(pydantic.BaseModel):
    route_prototype: entities.RoutePrototype
    departure_dates: list[datetime.datetime]

class UpdateRoutesDTO(pydantic.BaseModel):
    route: entities.Route

class AddPassengerDTO(pydantic.BaseModel):
    route_id: entities.HashId
    passenger: entities.Passenger

class PathInfoDTO(pydantic.BaseModel):
    move_from: entities.Spot
    move_to: entities.Spot
    price: int
    root_route_id: entities.HashId
    description: entities.MultiLanguages
    rules: entities.MultiLanguages
    transportation_rules: entities.MultiLanguages

class ShortRouteDTO(pydantic.BaseModel):
    move_from: entities.Place
    move_to: entities.Place
    count: int

class SpotTemplateDTO(pydantic.BaseModel):
    place: entities.Place
    from_start: int
    id: entities.HashId

class StartSpotTemplateDTO(pydantic.BaseModel):
    place: entities.Place
    id: entities.HashId

class RoutePrototypeDTO(pydantic.BaseModel):
    move_from: StartSpotTemplateDTO
    move_to: SpotTemplateDTO
    sub_spots: list[SpotTemplateDTO]
    passengers_number: int
    description: entities.MultiLanguages
    rules: entities.MultiLanguages
    transportation_rules: entities.MultiLanguages
    is_active: bool = True
    prices: entities.PricesSchema = {}
