@login_required
def get_owner_messages(request):
    try:
        owner = request.user.owner
    except Owner.DoesNotExist:
        return JsonResponse({'error': 'Owner account required'}, status=403)
    
    try:
        conversations = []
        seen_clients = set()
        
        # Get all messages for owner's rooms
        messages = Message.objects.filter(
            Q(room__owner=owner) & (Q(sender=request.user) | Q(receiver=request.user))
        ).order_by('-timestamp')
        
        for msg in messages:
            client_user = msg.sender if msg.sender != request.user else msg.receiver
            
            if client_user.id not in seen_clients:
                seen_clients.add(client_user.id)
                
                # Get latest message for this client
                latest_message = Message.objects.filter(
                    room__owner=owner,
                    Q(sender=client_user) | Q(receiver=client_user)
                ).order_by('-timestamp').first()
                
                if latest_message:
                    unread_count = Message.objects.filter(
                        room__owner=owner,
                        sender=client_user,
                        receiver=request.user,
                        read_status=False
                    ).count()
                    
                    try:
                        profile_image = client_user.userprofile.get_profile_image()
                    except:
                        profile_image = None
                    
                    conversations.append({
                        'room_id': latest_message.room.id,
                        'room_title': latest_message.room.title,
                        'client_name': client_user.get_full_name() or client_user.username,
                        'profile_image': profile_image,
                        'last_message': latest_message.content[:50] + ('...' if len(latest_message.content) > 50 else ''),
                        'last_message_time': latest_message.timestamp.isoformat(),
                        'unread_count': unread_count
                    })
        
        conversations.sort(key=lambda x: x['last_message_time'], reverse=True)
        return JsonResponse({'conversations': conversations})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)