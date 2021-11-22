from rest_framework import serializers
from .models import Reservation, Flight, Passenger

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'
        
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'
        
class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many = True, )
    flight_id = serializers.IntegerField() #normalde front end den gelecek
    user = serializers.StringRelatedField()
    user_id = serializers.IntegerField(required=False, write_only=True)
    
    class Meta:
        model= Reservation
        fields = (
            "id",
            "flight_id",
            "passenger",
            "user",
            "user_id"
        )
        
        def create(self, validated_data):
            print(validated_data)
            passenger_data = validated_data.pop('passenger') # ayrı bir model olduğu için gelen validated_data içinden passanger data yı aldık
            print(passenger_data)
            validated_data["user_id"] = self.context['request'].user.id
            reservation = Reservation.objects.create(**validated_data)
            for passenger in passenger_data:
                reservation.passenger.add(Passenger.objects.create(**passenger)) ##many to many field e add ile ekleme yapıyoruz..
            reservation.save()
            
            return reservation
            
            # [
            #     {
            #         first_name,
            #         last_name,
            #     }
            # ]
            
class StaffFlightSerializer(serializers.ModelSerializer):
    reservations = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields =(
            'flightNumber',
            'operatingAirlines',
            'departureCity',
            'arrivalCity'
            'dateOfDeparture',
            'estimatedTimeOfDeparture',
            'reservations'
        )