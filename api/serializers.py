from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import datetime
from events.models import Event , BookEvent

# ..........................signup............
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', ]
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        new_user = User(username=username, )
        new_user.set_password(password)
        new_user.save()
        return validated_data

class EventSerializer(serializers.ModelSerializer):
    # upcaoming_eventss=serializers.SerializerMethodField()
    class Meta:
        model = Event
        fields = '__all__'
        # fields =['title','description','organizer','date','price',tickets','event_type','location','time','logo']
    # def get_upcaoming_events(self,obj):
    #     events=Event.objects.filter(organizer=obj.organizer, date__gt=datetime.today())
    #     return EventSerializer(booking,many=True).data
class BookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEvent
        fields = '__all__'

class UpdateSerializer(serializers.ModelSerializer):
    class Meta :
        model = Event
        exclude = ['organizer',]

# class BookedSerializer(serializers.ModelSerializer):
#     # booker = serializers.SerializerMethodField()
#     class Meta :
#         model = BookEvent
#         fields =  '__all__'
#     # def get_booker(self,obj):
#     #     return BookEvent.objects.filter(booker=request.user)
#
# # class BookedSerializer(serializers.ModelSerializer):
#     booker = serializers.SerializerMethodField()
#     class Meta :
#         model = BookEvent
#         fields = ['booker']
#     def get_booker(self,obj):
#         return BookEvent.objects.filter(booker=request.user)
