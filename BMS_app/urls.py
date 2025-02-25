from django.urls import path, include
from rest_framework.routers import DefaultRouter
from BMS_app.views import UserView, MovieView, TheatreView, ShowView, BookingView

router = DefaultRouter()
router.register(r'users', UserView)
router.register(r'movies', MovieView)
router.register(r'theatres', TheatreView)
router.register(r'shows', ShowView)
router.register(r'bookings', BookingView)

urlpatterns = [
    path('', include(router.urls)),
]