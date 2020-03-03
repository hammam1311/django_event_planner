from django.shortcuts import render
from events.models import Event , BookEvent
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from .serializers import RegisterSerializer , EventSerializer , UpdateSerializer ,BookEventSerializer,EventTitleSerializer
from datetime import datetime
from rest_framework.permissions import IsAuthenticated , AllowAny
from .permissions import IsOrganizer







# ...................signup............
class Register(CreateAPIView):
    serializer_class = RegisterSerializer
# ................................list-Upcomig.....
class EventsList(ListAPIView):
    queryset = Event.objects.filter(date__gt=datetime.today().date())
    serializer_class = EventSerializer
    # permission_classes = [IsAuthenticated]
# ................................list-Organizer.....
class EventOrganizersList(ListAPIView):
    # queryset = Event.objects.filter(organizer=self.request.organizer)
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    def get_queryset(self):
        # self.check_permission(request)
        return Event.objects.filter(organizer=self.request.user)
    # needs an id
# .................................................................
class UpdateEvent(RetrieveUpdateAPIView):
    queryset = Event.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsAuthenticated, IsOrganizer, ]
    serializer_class = UpdateSerializer


class CreateEvent(CreateAPIView):
    serializer_class = EventTitleSerializer



class BookEventView(CreateAPIView):
    serializer_class = BookEventSerializer

class BookedList(ListAPIView):
    # queryset = BookEvent.objects.all()
    lookup_field = 'booker'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsAuthenticated]
    serializer_class = BookEventSerializer
    def get_queryset(self):
        return BookEvent.objects.filter(booker=self.request.user)
# no id needed



class MyBookers(ListAPIView):
    lookup_field = 'event'
    lookup_url_kwarg = 'event_id'
    permission_classes = [IsAuthenticated]
    serializer_class = BookEventSerializer
    def get_queryset(self):
        event_obj = Event.objects.get(id=self.kwargs.get("event_id"))
        return BookEvent.objects.filter(event= event_obj)
