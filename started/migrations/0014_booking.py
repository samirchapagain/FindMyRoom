# Generated migration for Booking model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('started', '0013_roomimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.client')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.owner')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.room')),
            ],
            options={
                'unique_together': {('client', 'room')},
            },
        ),
    ]