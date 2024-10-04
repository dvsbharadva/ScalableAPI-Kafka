from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from .models import Likes
from .kafka_producer import KafkaProducerServices
import time


def index(request):
    posts  = Likes.objects.all().values()
    # serializer = serializers.serialize('json', posts)
    return JsonResponse({
        'status' : True,
        'message' : list(posts)
    })

# Create your views here.
def likes(request, id: int):
    if id is None:
        return JsonResponse({
            'status' : False,
            'message' : 'ID is invalid'
        }) 
    producer = KafkaProducerServices(topic='locust-test-topic')
    producer.send_msg(key='post_id', msg=id)
    producer.close()
    return JsonResponse({
        'status' : True,
        'message' : 'like addded'        
    })
    
def send_kafka_msg(request, id: int):
    if id is None:
        return JsonResponse({
            'status' : False,
            'message' : 'ID is invalid'
        }) 
    producer = KafkaProducerServices(topic='locust-test-topic')
    producer.send_msg(key='post_id', msg=id)
    producer.close()
    return JsonResponse({
        'status' : True,
        'message' : 'Messag sent to kafka'
    })