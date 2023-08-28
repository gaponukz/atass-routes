import uuid
import datetime
import dataclasses

from src.domain.value_objects import HashId
from src.domain.value_objects import PricesSchema
from src.domain.value_objects import MultiLanguages

@dataclasses.dataclass
class Place:
    country: str
    city: str
    street: str
    map_url: str | None = None

@dataclasses.dataclass
class Spot:
    place: Place
    date: datetime.datetime
    is_active: bool = True
    id: HashId = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

@dataclasses.dataclass
class Passenger:
    full_name: str
    phone_number: str
    moving_from_id: HashId
    moving_towards_id: HashId
    gmail: str
    id: HashId
    is_anonymous: bool = True

@dataclasses.dataclass
class Route:
    passengers_number: int
    description: MultiLanguages
    rules: MultiLanguages
    transportation_rules: MultiLanguages
    move_from: Spot
    move_to: Spot
    is_active: bool = True
    prices: PricesSchema = dataclasses.field(default_factory=dict)
    sub_spots: list[Spot] = dataclasses.field(default_factory=list)
    passengers: list[Passenger] = dataclasses.field(default_factory=list)
    id: HashId = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

@dataclasses.dataclass
class Path:
    move_from: Spot
    move_to: Spot
    price: float
    root_route_id: HashId
