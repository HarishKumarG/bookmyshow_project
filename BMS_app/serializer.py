from django.utils import timezone
from rest_framework import serializers
from BMS_app.models import User, Movie, Theatre, Show, Booking


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

class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = '__all__'

    def validate_show_time(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Show time must be in the future.")
        return value


class BookingSerializer(serializers.ModelSerializer):
    booking_price = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = '__all__'

    def get_booking_price(self, obj):
        return obj.nooftickets * obj.show.ticket_price

    def validate(self, data):
        theatre = data.get('theatre')
        show = data.get('show')

        if not Show.objects.filter(id=show.id, theatre=theatre).exists():
            raise serializers.ValidationError("Selected show does not exist in the selected theatre.")
        return data