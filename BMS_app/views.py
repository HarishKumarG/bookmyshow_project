import uuid

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import User, Movie, Theatre, Screen, Show, Booking, Payment
from .serializer import UserSerializer, MovieSerializer, TheatreSerializer, ShowSerializer, BookingSerializer, \
    ScreenSerializer, PaymentSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class =UserSerializer

class MovieView(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class =MovieSerializer

class TheatreView(viewsets.ModelViewSet):
    queryset = Theatre.objects.all()
    serializer_class = TheatreSerializer

class ScreenView(viewsets.ModelViewSet):
    queryset = Screen.objects.all()
    serializer_class = ScreenSerializer

class ShowView(viewsets.ModelViewSet):
    queryset = Show.objects.all()
    serializer_class = ShowSerializer


class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "Booking confirmed successfully!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def validate_ticket(self, request, *args, **kwargs):
        data = request.data
        show_id = data.get("show")
        no_of_tickets = int(data.get("nooftickets", 0))

        # Ensure the show exists
        try:
            show = Show.objects.get(id=show_id)
        except Show.DoesNotExist:
            return Response({"error": "Invalid show ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Check ticket availability
        if show.total_tickets < no_of_tickets:
            return Response({"error": "Not enough tickets available"}, status=status.HTTP_400_BAD_REQUEST)

        # Deduct the tickets
        show.total_tickets -= no_of_tickets
        show.save()

        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            show=show,
            nooftickets=no_of_tickets,
            status="confirmed"
        )

        return Response(
            {"message": "Booking successful!", "data": BookingSerializer(booking).data},
            status=status.HTTP_201_CREATED
        )

class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        booking_id = data.get("booking")
        amount = data.get("amount")

        # Ensure the booking exists
        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking ID"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if payment already exists
        if Payment.objects.filter(booking=booking).exists():
            return Response({"error": "Payment already exists for this booking"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a transaction ID
        transaction_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            user=booking.booking_name,
            booking=booking,
            amount=amount,
            payment_method=data.get("payment_method"),
            status="completed",  # Assume payment is successful for now
            transaction_id=transaction_id,
        )

        return Response(
            {"message": "Payment successful!", "data": PaymentSerializer(payment).data},
            status=status.HTTP_201_CREATED
        )