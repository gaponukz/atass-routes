import pika
import json
import dataclass_factory
from urllib.parse import urlparse

from src.domain.events import PassengerPlaceEvent

class RabbitMQEventNotifier:
    def __init__(self, url: str):
        self._factory = dataclass_factory.Factory()
        self.connection = pika.BlockingConnection(self._connection_from_url(url))
        self.channel = self.connection.channel()

        self.channel.exchange_declare(exchange="events_exchange", exchange_type="direct")
        self.channel.queue_declare(queue="events")
        self.channel.queue_bind(exchange="events_exchange", queue="events", routing_key="passenger_events")

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

    def publish_event(self, event: PassengerPlaceEvent):
        self.channel.basic_publish(
            exchange="events_exchange",
            routing_key="passenger_events",
            body=json.dumps(self._factory.dump(event)),
            properties=pika.BasicProperties(
                content_type='application/json',
                delivery_mode=2
            )
        )

    def close(self):
        self.connection.close()
