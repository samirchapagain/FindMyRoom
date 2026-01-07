# Generated manually

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('started', '0011_populate_conversations'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.client')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.room')),
            ],
            options={
                'unique_together': {('client', 'room')},
            },
        ),
    ]