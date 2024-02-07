from django.test import TestCase
from django.core.validators import ValidationError
from books.models import Book


class BookModelTest(TestCase):

    def setUp(self):
        Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=10,
            daily_fee=12.34,
        )

    def test_inventory_positive_integer(self):
        book = Book.objects.get(id=1)
        self.assertTrue(book.inventory >= 0)

    def test_inventory_negative_integer_raise_error(self):
        book = Book.objects.get(id=1)
        book.inventory = -10

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_daily_fee_positive_decimal(self):
        book = Book.objects.get(id=1)
        self.assertTrue(book.daily_fee >= 0)

    def test_daily_fee_negative_decimal_raise_error(self):
        book = Book.objects.get(id=1)
        book.daily_fee = -0.1

        with self.assertRaises(ValidationError):
            book.full_clean()

    def test_daily_fee_decimal_places(self):
        book = Book.objects.get(id=1)
        self.assertEqual(book.daily_fee, round(book.daily_fee, 2))
