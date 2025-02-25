from django.urls import path, include
from rest_framework.routers import DefaultRouter
from BMS_app.views import UserView, MovieView, TheatreView, BookingView, ScreenView, ShowView, PaymentView

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'movies', MovieView)
router.register(r'theatres', TheatreView)
router.register(r'screens', ScreenView)
router.register(r'shows', ShowView)
router.register(r'bookings', BookingView)
router.register(r'payments', PaymentView)

urlpatterns = [
    path('', include(router.urls)),
]