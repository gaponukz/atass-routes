class RouteBusIsFullError(Exception):
    def __init__(self, max_passengers_number):
        self.max_passengers_number = max_passengers_number
        super().__init__(f"You try to add more than {max_passengers_number} passengers for route")

class CannotKillPassengersError(Exception):
    def __init__(self, passengers_number):
        self.passengers_number = passengers_number
        super().__init__(f"Already booked {passengers_number} places, cannot set value, remove few")

class PassengerNotFoundError(Exception):
    def __init__(self):
        super().__init__("Can not find passenger with that identifier")

class SpotNotFoundError(Exception):
    def __init__(self, route_id: str, spot_id: str):
        super().__init__(f"Can not find spot {spot_id} in route {route_id}")

class RouteNotFoundError(Exception):
    def __init__(self, route_id: str):
        self.route_id = route_id
        super().__init__(f"Can not find route with identifier {route_id}")

class PaymentDuplicationError(Exception):
    def __init__(self, payment_id: str):
        self.payment_id = payment_id
        super().__init__(f"Paymend {payment_id} is duplicate")
