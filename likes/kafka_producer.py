from confluent_kafka import Producer
import json
import logging

class KafkaProducerServices:
    def __init__(self, topic, kafka_config=None):
        if kafka_config is None:
            kafka_config = {
                'bootstrap.servers': 'localhost:9092',
                'client.id': 'locust-testing-producer'
            }
        self.producer = Producer(kafka_config)
        self.topic = topic
        self.logger = logging.getLogger(__name__)

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"Message delivery failed {err}")
        else:
            self.logger.info(f"Message delivered to {msg.topic()} - [{msg.partition()}]")

    def send_msg(self, key, msg):
        try:
            print("Producing message...")
            self.producer.produce(
                self.topic,
                key=key.encode('utf-8'),
                value=json.dumps({"post_id": msg}),
                callback=self.delivery_report
            )
            self.producer.flush()  # Ensure this is called correctly
            self.logger.info(f"Message sent successfully to {self.topic}")

        except Exception as e:
            self.logger.error(f"Error while sending: {str(e)}")

    def close(self):
        self.producer.flush()
