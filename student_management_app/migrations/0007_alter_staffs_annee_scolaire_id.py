# Generated by Django 4.2.13 on 2024-10-25 09:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("student_management_app", "0006_alter_semaines_annee_scolaire_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="staffs",
            name="annee_scolaire_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="student_management_app.anneescolaire",
            ),
        ),
    ]
