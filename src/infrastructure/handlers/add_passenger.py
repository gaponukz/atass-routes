import time
import json
import typing
import pika
import multiprocessing

from src.domain.entities import Passenger
from src.domain.events import PaymentProcessed
from src.application.dto import NotifyPassengerDTO
from urllib.parse import urlparse

class AddPassengerService(typing.Protocol):
    def add_passenger(self, event: PaymentProcessed): ...

class PassengerNotifier(typing.Protocol):
    def notify(self, data: NotifyPassengerDTO): ...

class RoutesEventsListener:
    def __init__(
            self,
            add_passenger_service: AddPassengerService,
            notify_passenger_service: PassengerNotifier,
            url: str
        ):
        
        self.add_passenger_service = add_passenger_service
        self.notify_passenger_service = notify_passenger_service

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
            credentials=credentials,
            heartbeat=10
        )
    
    def process_message(self, message: str):
        data = json.loads(message)
        passenger_json = data['passenger']

        passenger = Passenger(
            full_name=passenger_json['fullName'],
            phone_number=passenger_json['phoneNumber'],
            moving_from_id=passenger_json['movingFromId'],
            moving_towards_id=passenger_json['movingTowardsId'],
            email_address=passenger_json['gmail'],
            id=passenger_json['id'],
            is_anonymous=passenger_json.get('isAnonymous', False),
        )

        self.add_passenger_service.add_passenger(PaymentProcessed(
            route_id=data['routeId'],
            passenger=passenger
        ))

        self.notify_passenger_service.notify(NotifyPassengerDTO(
            payment_id=data['paymentId'],
            passenger=passenger
        ))

    def _callback(self, ch, method, properties, body):
        self.process_message(body)
        
    def listen(self):
        multiprocessing.Process(target=self._listen).start()

    def _listen(self):
        while True:
            try:
                self.channel.basic_consume(queue="route_payments", on_message_callback=self._callback, auto_ack=True)
                self.channel.start_consuming()
            except pika.exceptions.ConnectionClosed:
                self.reconnect()

    def reconnect(self):
        attempts = 0
        while not self.connection.is_closed and attempts < 3:
            try:
                self.connection.close()
            except:
                pass

            try:
                self.connection = pika.BlockingConnection(self._connection_from_url(self.url))
                self.channel = self.connection.channel()
                self.channel.queue_bind(exchange="payments_exchange", queue="route_payments")
                return
            
            except:
                time.sleep(5)
                attempts += 1

    def close(self):
        self.channel.close()
        self.connection.close()
