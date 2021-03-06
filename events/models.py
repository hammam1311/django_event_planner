from django.db import models
from django.contrib.auth.models import User

class Event (models.Model) :
    EVENT_TYPE =(
        ("Educational", "Educational"),
        ("Musical", "Musical"),
        ("Comedy", "Comedy"),
        )
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=255, null = True , blank = True)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null = True , blank = True)
    date = models.DateField( null = True , blank = True)
    price = models.DecimalField(max_digits=5,decimal_places=2, null = True , blank = True)
    tickets = models.PositiveIntegerField(null = True , blank = True)
    event_type = models.CharField(max_length=25,choices = EVENT_TYPE,null = True , blank = True)
    location = models.CharField(max_length=120,null = True , blank = True)
    time = models.TimeField(null = True , blank = True)
    logo = models.ImageField(upload_to='event_logos', null=True, blank=True)
    def __str__(self):
        return self.title

class BookEvent(models.Model):
    booker = models.ForeignKey(User, on_delete=models.CASCADE,  blank = True,null = True ,)
    number_of_tickets = models.PositiveIntegerField(null = True , blank = True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null = True , blank = True ,)

class Profile(models.Model):
    EVENT_TYPE =(
        ("Educational", "Educational"),
        ("Musical", "Musical"),
        ("Comedy", "Comedy"),
        )
    firstname=models.CharField(max_length=120)
    lastname =models.CharField(max_length=120)
    intrests =models.CharField(max_length=25,choices = EVENT_TYPE,null = True , blank = True)
    image = models.ImageField(upload_to='event_logos', null=True, blank=True)
    username =models.ForeignKey(User, on_delete=models.CASCADE,  blank = True,null = True ,)
    # .........................e7tyat
