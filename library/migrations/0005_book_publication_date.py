# Generated by Django 5.1.3 on 2024-11-11 18:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0004_remove_book_cover_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="publication_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]