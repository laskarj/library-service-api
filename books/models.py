from django.core.validators import MinValueValidator
from django.db import models


class Book(models.Model):
    """
    Model representing a book.

    Attributes:
        title (str): The title of the book.
        author (str): The author of the book.
        cover (str): The type of cover of the book (choices: "HARD", "SOFT").
        inventory (int): The number of copies of the book available in the
        library (must be a non-negative integer).
        daily_fee (Decimal): The daily fee for borrowing the book in USD
        (must be a non-negative decimal with up to 2 decimal places).
    """

    COVER_CHOICES = (
        ("HARD", "Hard cover"),
        ("SOFT", "Soft cover"),
    )

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=16, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )
