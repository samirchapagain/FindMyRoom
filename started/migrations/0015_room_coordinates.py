# Generated migration for Room location coordinates

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('started', '0014_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=11, max_digits=11, null=True),
        ),
    ]