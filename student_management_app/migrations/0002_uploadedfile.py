# Generated by Django 4.2.13 on 2024-10-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student_management_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UploadedFile",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file", models.FileField(upload_to="uploads/")),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
