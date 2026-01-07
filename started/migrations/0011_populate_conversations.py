# Data migration to populate conversations from existing messages

from django.db import migrations
from django.db.models import Q


def populate_conversations(apps, schema_editor):
    Message = apps.get_model('started', 'Message')
    Conversation = apps.get_model('started', 'Conversation')
    Client = apps.get_model('started', 'Client')
    Owner = apps.get_model('started', 'Owner')
    
    # Get all unique client-owner-room combinations from existing messages
    messages = Message.objects.all()
    conversations_created = set()
    
    for message in messages:
        try:
            # Determine client and owner from sender/receiver
            if hasattr(message.sender, 'client'):
                client_user = message.sender
                owner_user = message.receiver
            elif hasattr(message.receiver, 'client'):
                client_user = message.receiver
                owner_user = message.sender
            else:
                continue
            
            client = Client.objects.get(user=client_user)
            owner = Owner.objects.get(user=owner_user)
            
            # Create unique key for this conversation
            conv_key = (client.id, owner.id, message.room.id)
            
            if conv_key not in conversations_created:
                # Create conversation
                conversation, created = Conversation.objects.get_or_create(
                    client=client,
                    owner=owner,
                    room=message.room
                )
                conversations_created.add(conv_key)
                
                # Update all messages for this conversation
                Message.objects.filter(
                    room=message.room
                ).filter(
                    Q(sender=client_user, receiver=owner_user) | 
                    Q(sender=owner_user, receiver=client_user)
                ).update(conversation=conversation)
                
        except (Client.DoesNotExist, Owner.DoesNotExist):
            continue


def reverse_populate_conversations(apps, schema_editor):
    # Remove conversation references
    Message = apps.get_model('started', 'Message')
    Message.objects.all().update(conversation=None)


class Migration(migrations.Migration):

    dependencies = [
        ('started', '0010_add_conversation_model'),
    ]

    operations = [
        migrations.RunPython(populate_conversations, reverse_populate_conversations),
    ]