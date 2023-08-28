import datetime
import dataclasses
from src.domain.entities import Route
from src.domain.entities import Spot
from src.domain.entities import Passenger
from src.domain.entities import Place

from src.domain.value_objects import DayDate
from src.domain.value_objects import HashId
from src.domain.value_objects import MultiLanguages
from src.domain.value_objects import PricesSchema

@dataclasses.dataclass
class GetAviableRoutesDTO:
    move_from_city: str
    move_to_city: str
    date: DayDate

@dataclasses.dataclass
class UpdateRoutesDTO:
    route: Route

@dataclasses.dataclass
class PathInfoDTO:
    move_from: Spot
    move_to: Spot
    price: float
    root_route_id: HashId
    description: MultiLanguages
    rules: MultiLanguages
    transportation_rules: MultiLanguages

@dataclasses.dataclass
class ShortRouteDTO:
    move_from: Place
    move_to: Place
    count: int

@dataclasses.dataclass
class SubSpotTemplateDTO:
    place: Place
    from_start: int
    id: HashId

@dataclasses.dataclass
class SpotTemplateDTO:
    place: Place
    id: HashId

@dataclasses.dataclass
class RoutePrototypeDTO:
    move_from: SpotTemplateDTO
    move_to: SpotTemplateDTO
    sub_spots: list[SubSpotTemplateDTO]
    passengers_number: int
    description: MultiLanguages
    rules: MultiLanguages
    transportation_rules: MultiLanguages
    is_active: bool = True
    prices: PricesSchema = dataclasses.field(default_factory=dict)

@dataclasses.dataclass
class AddRoutesDTO:
    route_prototype: RoutePrototypeDTO
    departure_dates: list[tuple[datetime.datetime, datetime.datetime]]

@dataclasses.dataclass
class AddPassengerDTO:
    payment_id: HashId
    route_id: HashId
    passenger: Passenger

@dataclasses.dataclass
class NotifyPassengerDTO:
    payment_id: HashId
    passenger: Passenger
