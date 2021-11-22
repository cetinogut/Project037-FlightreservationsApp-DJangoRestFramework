from django.shortcuts import render
from .models import Flight, Reservation, Passenger
from .serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from rest_framework import viewsets, filters
from .permissions import IsStuffOrReadOnly
from datetime import datetime, date


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permisisons_class=(IsStuffOrReadOnly,)
    filter_backends= (filters.SearchFilter,) ##added for search
    search_fields = ('departureCity', 'arrivalCity', 'dateOfDeparture')
    
    def get_serializer_class(self):
        if self.request.user.is_staff:
            return super().get_serializer_class()
        else:
            return FlightSerializer
        
    def get_queryset(self): # geçmiş uçuşlarına ihtiyaç yok, bunları normal kullanıcılar görmesin diye override ettik
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print('Current time:', current_time)
        today = date.today()
        print ("Today :", today)
        
        if self.request.user.is_staff: # admin aşağıdaki satırla FlightView in 10. satırdaki queryset ine ulaşacak ve hepsini görecek
            return super().get_queryset()
        else: # normal kullanıcılar aşağıda bugün ve bu saate göre filtrelenene seti görecek
            queryset = Flight.objects.filter(dateOfDeparture__gte=today).filter(estimatedTimeOfDeparture__gt=current_time)
    
class ReservationView(viewsets.ModelViewSet):
   queryset = Flight.objects.all()
   serializer_class = ReservationSerializer
   
   def get_queryset(self): # bunu override ettik GenericAPIViewden geliyor
       queryset = super().get_queryset() # yukarıdaki queryset i aldık
       if self.request.user.is_staff:
           return queryset
       return queryset.filter(user=self.request.user) 
       