from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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

    class CoverChoices(models.TextChoices):
        HARD = "HARD", _("Hard cover")
        SOFT = "SOFT", _("Soft cover")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=CoverChoices.choices)
    inventory = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    daily_fee = models.DecimalField(
        max_digits=8, decimal_places=2, validators=[MinValueValidator(0)]
    )

    def __str__(self) -> str:
        return (
            f"Title: {self.title};\n Author: {self.author};\n"
            f" Cover: {self.cover};\n Inventory: {self.inventory}"
        )
