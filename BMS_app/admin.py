from django.contrib import admin
from BMS_app.models import User, Movie, Theatre, Show, Booking

# Register your models here.
admin.site.register(User)
admin.site.register(Movie)
admin.site.register(Theatre)
admin.site.register(Show)
admin.site.register(Booking)