from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    publication_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title or "Book"

class Newspaper(models.Model):
    editorial = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Newspaper - {self.date or 'Unknown Date'}"

