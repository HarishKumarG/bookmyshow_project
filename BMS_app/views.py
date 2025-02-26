import uuid
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Movie, Theatre, Screen, Show, Booking, Payment, Seat
from .serializer import UserSerializer, MovieSerializer, TheatreSerializer, ShowSerializer, BookingSerializer, ScreenSerializer, PaymentSerializer, SeatSerializer


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
        data = request.data
        serializer = self.get_serializer(data=data)

        if serializer.is_valid():
            show = serializer.validated_data['show']
            no_of_tickets = serializer.validated_data['nooftickets']

            if show.reduce_available_seats(no_of_tickets):
                self.perform_create(serializer)
                return Response(
                    {"message": "Booking Initiated! Complete the payment!", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                if show.available_seats <= 0:
                    return Response(
                        {"error": "All seats are booked for this show."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                else:
                    return Response(
                        {"error": f"Only {show.available_seats} seats are available for this show."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'post'])
    def cancel(self, request, pk=None):
        try:
            booking = self.get_object()
            booking.cancel_booking()
            return Response({"message": "Booking canceled and seats restored."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

class PaymentView(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        booking_id = data.get("booking")
        amount = data.get("amount")

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking ID"}, status=status.HTTP_400_BAD_REQUEST)

        if Payment.objects.filter(booking=booking).exists():
            return Response({"error": "Payment already exists for this booking"}, status=status.HTTP_400_BAD_REQUEST)

        if not amount:
            amount = booking.nooftickets * booking.show.ticket_price

        transaction_id = str(uuid.uuid4())

        payment = Payment.objects.create(
            user=booking.booking_name,
            booking=booking,
            amount=amount,
            payment_method=data.get("payment_method"),
            status=data.get("status"),
            transaction_id=transaction_id,
        )
        if payment.status == "completed":
            return Response(
                {"message": "Payment successful! Booking Confirmed", "data": PaymentSerializer(payment).data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"message": "Payment not confirmed!", "data": PaymentSerializer(payment).data},
                status=status.HTTP_201_CREATED
            )


class SeatLayoutView(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    def get_queryset(self):
        """
        Override get_queryset to filter seats by the show.
        """
        show_id = self.kwargs.get('pk')  # This assumes that the pk is the show ID.
        return Seat.objects.filter(show_id=show_id)

    def list(self, request, *args, **kwargs):
        """
        Handle the list view for seats. This will return all seats for the specified show.
        """
        show_id = kwargs.get('pk')
        try:
            show = Show.objects.get(pk=show_id)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

        seats = self.get_queryset()
        serializer = self.get_serializer(seats, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Handle seat creation. We assume that the seat information (row, column) is passed in.
        """
        show_id = kwargs.get('pk')
        try:
            show = Show.objects.get(pk=show_id)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

        # Add show_id to the request data before passing to the serializer
        request.data['show'] = show.id
        return super().create(request, *args, **kwargs)


class BookingView(viewsets.ModelViewSet):
    queryset = Booking.objects.all()  # This will be used by the viewset for list, create, etc.
    serializer_class = BookingSerializer

    # Custom Create method (you can keep it if you need to customize further)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(
                {"message": "Booking confirmed!", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CancelBookingView(APIView):
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            booking.cancel_booking()
            return Response({"message": "Booking canceled and seats reverted to available."}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

class SeatSelectionView(APIView):
    def get(self, request, pk=None):
        try:
            show = Show.objects.get(pk=pk)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

        seats = Seat.objects.filter(show=show)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        try:
            show = Show.objects.get(pk=pk)
        except Show.DoesNotExist:
            return Response({"error": "Show not found."}, status=status.HTTP_404_NOT_FOUND)

        seat_id = request.data.get("seat_id")
        try:
            seat = Seat.objects.get(pk=seat_id, show=show)
        except Seat.DoesNotExist:
            return Response({"error": "Seat not found."}, status=status.HTTP_404_NOT_FOUND)

        if seat.is_booked:
            return Response({"error": "Seat already booked."}, status=status.HTTP_400_BAD_REQUEST)

        seat.is_booked = True
        seat.save()

        return Response({"message": "Seat booked successfully!"}, status=status.HTTP_200_OK)