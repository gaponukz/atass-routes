import json
import typing
import threading
import pika

from src.business.entities import Passenger
from src.business.dto import AddPassengerDTO
from urllib.parse import urlparse

class AddPassengerService(typing.Protocol):
    def add_passenger(self, data: AddPassengerDTO): ...

class RoutesEventsListener:
    def __init__(self, service: AddPassengerService, url: str):
        self.service = service
        self.connection = pika.BlockingConnection(self._connection_from_url(url))
        self.channel = self.connection.channel()
        self.channel.queue_bind(exchange="payments_exchange", queue="route_payments")

    def _connection_from_url(self, url: str) -> pika.ConnectionParameters:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in ('amqp', 'amqps'):
            raise ValueError("Invalid URL scheme. Only 'amqp' and 'amqps' schemes are supported.")

        credentials = None
        if parsed_url.username and parsed_url.password:
            credentials = pika.PlainCredentials(parsed_url.username, parsed_url.password)

        return pika.ConnectionParameters(
            host=parsed_url.hostname or "localhost",
            port=parsed_url.port or 5672,
            virtual_host=parsed_url.path.strip('/') or '/',
            credentials=credentials
        )
    
    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        passenger_json = data['passenger']

        self.service.add_passenger(AddPassengerDTO(
            route_id=data.get('routeId'),
            passenger=Passenger(
                full_name=passenger_json['fullName'],
                phone_number=passenger_json['phoneNumber'],
                moving_from_id=passenger_json['movingFromId'],
                moving_towards_id=passenger_json['movingTowardsId'],
                email_address=passenger_json['gmail'],
                id=passenger_json['id']
            )
        ))
    
    def listen(self):
        threading.Thread(target=self._listen).start()

    def _listen(self):
        self.channel.basic_consume(queue="route_payments", on_message_callback=self.callback, auto_ack=True)
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()
