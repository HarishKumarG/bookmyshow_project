from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Show, Seat

@receiver(post_save, sender=Show)
def create_seats_for_show(sender, instance, created, **kwargs):
    if created:
        # Creating 100 seats (10 rows x 10 columns)
        for row in range(1, 11):  # Rows 1 to 10
            for column in range(1, 11):  # Columns 1 to 10
                Seat.objects.create(show=instance, row=row, column=column)
