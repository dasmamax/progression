# Generated by Django 4.2.13 on 2024-10-28 03:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("student_management_app", "0007_alter_staffs_annee_scolaire_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffs",
            name="annee_scolaire_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="student_management_app.anneescolaire",
            ),
        ),
    ]
