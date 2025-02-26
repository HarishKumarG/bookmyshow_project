from django.urls import path, include
from rest_framework.routers import DefaultRouter
from BMS_app.views import UserView, MovieView, TheatreView, BookingView, ScreenView, ShowView, PaymentView, \
    SeatLayoutView, CancelBookingView, SeatSelectionView

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'movies', MovieView)
router.register(r'theatres', TheatreView)
router.register(r'screens', ScreenView)
router.register(r'shows', ShowView)
router.register(r'bookings', BookingView)
router.register(r'payments', PaymentView)
router.register(r'seats', SeatLayoutView)
urlpatterns = [
    path('', include(router.urls)),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='cancel-booking'),
    path('shows/<int:pk>/seats/', SeatSelectionView.as_view(), name='seat-selection'),
]