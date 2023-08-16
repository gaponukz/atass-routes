import typing
import dataclasses
from src.domain.entities import Passenger
from src.domain.value_objects import HashId

@dataclasses.dataclass
class PaymentProcessed:
    route_id: HashId
    passenger: Passenger

@dataclasses.dataclass
class PassengerPlaceEvent:
    type: typing.Literal['booked', 'removed']
    route_id: HashId
    move_from_id: HashId
    move_to_id: HashId
    passenger_id: HashId
