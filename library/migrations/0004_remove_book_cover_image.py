# Generated by Django 5.1.3 on 2024-11-11 18:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("library", "0003_remove_newspaper_front_page_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="book",
            name="cover_image",
        ),
    ]