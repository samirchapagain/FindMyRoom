# Generated manually for Conversation model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('started', '0009_userprofile_pin_created_at_userprofile_reset_pin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.client')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.owner')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='started.room')),
            ],
            options={
                'unique_together': {('client', 'owner', 'room')},
            },
        ),
        migrations.AddField(
            model_name='message',
            name='conversation',
            field=models.ForeignKey(null=True, blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='started.conversation'),
        ),
    ]