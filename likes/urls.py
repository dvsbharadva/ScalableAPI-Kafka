from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="home" ),
    path('like/<int:id>', views.likes, name="like"),
]