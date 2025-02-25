from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class User(models.Model):
    username = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)
    mobile = PhoneNumberField()
    location = models.CharField(max_length=100, blank=True)
    ismember = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'email', 'mobile']

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.username

class Movie(models.Model):
    title = models.CharField(max_length=100)
    language = models.CharField()
    genre = models.CharField()

    class Meta:
        ordering = ["id"]
        unique_together = (('title', 'language'),)

    def __str__(self):
        return self.title

class Theatre(models.Model):
    theatre_name = models.CharField()
    noofseats = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    location = models.CharField()

    class Meta:
        unique_together = (('theatre_name', 'location'),)

    def __str__(self):
        return f"Id:{self.id} {self.theatre_name} {self.location}"


class Show(models.Model):
    show_number = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name='show_movie')
    theatre = models.ForeignKey("Theatre", on_delete=models.CASCADE, related_name='show_theatre')
    show_time = models.DateTimeField()
    ticket_price = models.PositiveIntegerField(default=150, validators=[MinValueValidator(150), MaxValueValidator(200)])

    class Meta:
        unique_together = (('show_number', 'theatre', 'show_time'),)

    def __str__(self):
        return f"Show: {self.show_number} Theatre: {self.theatre.id} {self.theatre.theatre_name} Movie: {self.movie.title}"

class Booking(models.Model):
    booking_name = models.ForeignKey("User", on_delete=models.CASCADE, related_name='booking_user')
    nooftickets = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    theatre = models.ForeignKey("Theatre", on_delete=models.CASCADE, related_name='booking_theatre')
    show = models.ForeignKey("Show", on_delete=models.CASCADE, related_name='booking_show')

    def __str__(self):
        return f"{self.booking_name} Show: {self.show.show_number} Theatre: {self.theatre.theatre_name}"



