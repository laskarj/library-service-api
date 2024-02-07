from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    COVER_CHOICES = (
        ("HARD", "Hard cover"),
        ("SOFT", "Soft cover"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=16, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
