import json
import typing
import pika

from src.business.entities import Passenger
from src.business.dto import AddPassengerDTO

class AddPassengerService(typing.Protocol):
    def add_passenger(self, data: AddPassengerDTO): ...

class RoutesEventsListener:
    def __init__(self, service: AddPassengerService, rabbitUrl: str):
        self.service = service
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitUrl))
        self.channel = self.connection.channel()
        self.channel.queue_bind(exchange="payments_exchange", queue="payments")

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        passenger_json = data['passenger']

        self.service.add_passenger(AddPassengerDTO(
            route_id=data.get('routeId') or data.get('route_id'),
            passenger=Passenger(
                full_name=passenger_json.get('fullName') or passenger_json.get('full_name'),
                phone_number=passenger_json.get('phoneNumber') or passenger_json.get('phone_number') or passenger_json.get('phone'),
                moving_from_id=passenger_json.get("movingFromId") or passenger_json.get("moving_from_id"),
                moving_towards_id=passenger_json.get("movingTowardsId") or passenger_json.get('moving_towards_id'),
                email_address=passenger_json.get('emailAddress') or passenger_json.get('gmail'),
                id=passenger_json.get('id', '')
            )
        ))

    def listen(self):
        self.channel.basic_consume(queue="payments", on_message_callback=self.callback, auto_ack=True)
        print("Listening for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
