from confluent_kafka import Consumer
import json
import logging
from collections import defaultdict
from django.db import transaction
from .models import Likes

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
class KafkaConsumerServices:
    def __init__(self, topic, kafka_cofig=None):
        if kafka_cofig is None:
            kafka_cofig = {
                'bootstrap.servers' : 'localhost:9092',
                'group.id':'locust-testing-group',
                'auto.offset.reset' : 'earliest'
            }
        self.consumer = Consumer(kafka_cofig)
        self.topic = topic
        self.logger = logging.getLogger(__name__)
        self.consumer.subscribe([self.topic])
        
  
    def process_msg(self, msg):
        with transaction.atomic():
            post = Likes.objects.get(id=msg)
            post.like += 1
            post.save()
            self.logger.info(f"Data saved to db: ")
            
               

    def consume_msg(self):
        print("consumer started..")
        total_msg =0
        list_batch = defaultdict(int)
        try:
            while True:
                self.logger.info("Polling for messages...")
                msg = self.consumer.poll(timeout=10.0)  # Increase the timeout
                if msg is None:
                    self.logger.info("No message received in the current poll.")
                    continue
                if msg.error():
                    self.logger.error(f"Consumer error: {msg.error()}")
                    continue
               
                self.logger.info("message received")
                data = json.loads(msg.value().decode('utf-8'))
                post_id = data['post_id']
                self.process_msg(post_id)
                
        except Exception as e:
            self.logger.error(f"Error while consuming message: {str(e)}")
        
    def close(self):
        self.consumer.close()