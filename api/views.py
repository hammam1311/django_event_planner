from django.shortcuts import render
from events.models import Event , BookEvent
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from .serializers import RegisterSerializer , EventSerializer
from datetime import datetime



# ...................signup............
class Register(CreateAPIView):
	serializer_class = RegisterSerializer
# ................................list-Upcomig.....
class EventsList(ListAPIView):
	queryset = Event.objects.filter(date__gt=datetime.today().date())
	serializer_class = EventSerializer
