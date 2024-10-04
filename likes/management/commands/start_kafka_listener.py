from django.core.management.base import BaseCommand
from likes.kafka_consumer import KafkaConsumerServices


class Command(BaseCommand):
    help = "Consume msg from kafka"
    
    def handle(self, *args, **kwargs):

        consumer = KafkaConsumerServices(topic='locust-test-topic')
        try:
            self.stdout.write(self.style.SUCCESS("Starting kafka consumer.."))
            consumer.consume_msg()
            print("consumer msg exec")
        except Exception as e:
            self.stdout.write(self.style.WARNING("Consumer stopped.."))
        finally:
            consumer.close()
            pass