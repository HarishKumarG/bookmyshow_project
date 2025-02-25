from rest_framework import viewsets
from .models import User, Movie, Theatre, Show, Booking
from .serializer import UserSerializer, MovieSerializer, TheatreSerializer, ShowSerializer, BookingSerializer

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class =UserSerializer

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class =MovieSerializer

class TheatreView(viewsets.ModelViewSet):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer

class ShowView(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
