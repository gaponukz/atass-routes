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

class Logger(typing.Protocol):
    def info(self, message: str): ...

    def warn(self, message: str): ...

class RoutesEventsListener:
    def __init__(
            self,
            add_passenger_service: AddPassengerService,
            notify_passenger_service: PassengerNotifier,
            logger: Logger,
            url: str
        ):
        
        self.url = url
        self.add_passenger_service = add_passenger_service
        self.notify_passenger_service = notify_passenger_service
        self.logger = logger

        self.connection = pika.BlockingConnection(self._connection_from_url(url))
        self.channel = self.connection.channel()
        self.channel.queue_bind(exchange="payments_exchange", queue="route_payments")
        self.logger.info("Successfully connected to rabbitmq from __init__")

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
        self.logger.info(f'Processing message: "{message[:10]}..."')
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

        self.logger.info(f"Successfully parsed passenger {passenger_json['id']} from event")

        self.add_passenger_service.add_passenger(PaymentProcessed(
            route_id=data['routeId'],
            passenger=passenger
        ))

        self.logger.info(f"Successfully added passenger {passenger_json['id']}")

        self.notify_passenger_service.notify(NotifyPassengerDTO(
            payment_id=data['paymentId'],
            passenger=passenger
        ))

        self.logger.info(f"Successfully notified passenger {passenger_json['id']}")

    def _callback(self, ch, method, properties, body):
        try:
            self.process_message(body)
        
        except Exception as error:
            self.logger.warn(f"Can not process message, {error.__class__.__name__}: {error}")
    
    def listen(self):
        multiprocessing.Process(target=self._listen).start()

    def _listen(self):
        while True:
            try:
                self.channel.basic_consume(queue="route_payments", on_message_callback=self._callback)
                self.channel.start_consuming()
            
            except Exception as error:
                self.logger.warning(f"Connection closed in _listen, {error.__class__.__name__}: {error}")
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
                self.logger.info("Successfully reconnected")
                return
            
            except:
                self.logger.info("Sleep 5 seconds before reconnect")
                time.sleep(5)
                attempts += 1

    def close(self):
        self.channel.close()
        self.connection.close()
