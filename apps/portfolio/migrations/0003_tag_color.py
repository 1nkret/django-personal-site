# Generated by Django 5.1.6 on 2025-02-12 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("portfolio", "0002_tag_project_tags"),
    ]

    operations = [
        migrations.AddField(
            model_name="tag",
            name="color",
            field=models.CharField(
                default="#007bff",
                help_text="Выберите цвет в формате HEX (например, #ff5733)",
                max_length=7,
            ),
        ),
    ]
