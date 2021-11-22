from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flight(models.Model):
    flightNumber = models.IntegerField()
    operatingAirlines = models.CharField(max_length=25)
    departureCity = models.CharField(max_length=30)
    arrivalCity = models.CharField(max_length=30)
    dateOfDeparture = models.DateField()
    estimatedTimeOfDeparture = models.TimeField()
    
    ordering = ['flightNumber']
    
    def __str__(self):
        return f"{self.operatingAirlines} {self.flightNumber} {self.departureCity[0:3].upper()}-{self.arrivalCity[0:3].upper()}"
    
class Passenger(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=60)
    email = models.EmailField()
    phoneNumber = models.IntegerField()
    updatedDate = models.DateTimeField(auto_now=True)
    createdDate = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.firstName} - {self.lastName}" 
    
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    passenger = models.ManyToManyField(Passenger, related_name='passenger')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='reservations') # bununla flight ın reservations ına ulaşabileceiz
    
    
    def __str__(self):
        return f"{self.flight} {self.passenger} - {self.user}"