# Generated by Django 4.2.16 on 2024-11-14 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_delete_eventregistration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='additionalitemevent',
            name='distance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='additional_options', to='event.distanceevent'),
            preserve_default=False,
        ),
    ]