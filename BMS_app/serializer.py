from django.utils import timezone
from rest_framework import serializers
from BMS_app.models import User, Movie, Theatre, Show, Booking, Screen, Payment, Seat


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class TheatreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theatre
        fields = '__all__'

class ScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screen
        fields = '__all__'


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ['id', 'row', 'column', 'is_booked']

class ShowSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(many=True, read_only=True)
    class Meta:
        model = Show
        fields = '__all__'

    def validate(self, data):
        screen = data.get('screen')
        show_time = data.get('show_time')

        if Show.objects.filter(screen=screen, show_time=show_time).exists():
            raise serializers.ValidationError("Another show is already scheduled at this time on this screen.")
        return data

    def validate_show_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Show time must be in the future.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    booking_price = serializers.SerializerMethodField()
    selected_seats = serializers.ListField(child=serializers.IntegerField(), required=True)

    class Meta:
        model = Booking
        fields = ['id', 'booking_name', 'booking_price', 'nooftickets', 'show', 'selected_seats']

    def get_booking_price(self, obj):
        return obj.nooftickets * obj.show.ticket_price

    def validate(self, data):
        theatre = data.get('theatre')
        show = data.get('show')
        selected_seats = data.get('selected_seats')

        if show.theatre != theatre:
            raise serializers.ValidationError(f"Wrong Show '{show}' selected for the theatre '{theatre}'")

        seats = Seat.objects.filter(id__in=selected_seats, show=show)
        if len(seats) != len(selected_seats):
            raise serializers.ValidationError("Some of the selected seats are not available or do not exist.")

        # Ensure seats are available
        for seat in seats:
            if seat.status != 'available':
                raise serializers.ValidationError(f"Seat {seat.row}{seat.column} is already booked.")
        return data

    def create(self, validated_data):
        selected_seats = validated_data.pop('selected_seats')
        booking = super().create(validated_data)

        # Change seat status to 'booked'
        seats = Seat.objects.filter(id__in=selected_seats)
        seats.update(status='booked')

        booking.selected_seats.set(seats)
        return booking


class PaymentSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = '__all__'

    def get_amount(self, obj):
        return obj.amount

    def get_booking_price(self, obj):
        if obj.booking:
            return obj.booking.nooftickets * obj.booking.show.ticket_price
        return None

