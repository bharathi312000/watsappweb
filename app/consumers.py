import json
from channels.generic.websocket import AsyncWebsocketConsumer 
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from app.models import Mychats
from django.contrib.auth.models import User
import datetime
from channels.db import database_sync_to_async


class MychatApp(AsyncWebsocketConsumer):
    
    async def connect(self):
        user = self.scope['user']
        print(f"Connecting user: {user}")

        # Ensure that the user is authenticated
        if user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(f"mychat_app_{user}", self.channel_name)
        else:
            await self.close()

    async def disconnect(self, close_code): 
        user = self.scope['user']
        await self.channel_layer.group_discard(f"mychat_app_{user}", self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data = json.loads(text_data)
        print(text_data,"textdata")
        # Send message to the specific chat group
        await self.channel_layer.group_send(
            f"mychat_app_{text_data['user']}",
            {
                'type': 'send.msg',
                'msg': text_data['msg'],
                'sender': self.scope['user'].username

            }
        )

        # Save the message to the database
        await self.save_chat(text_data)

    @database_sync_to_async
    def save_chat(self, text_data):
        print(text_data,'from save_chat')
        try:
            frnd = User.objects.get(username=text_data['user'])
            now = datetime.datetime.now()

            # Format time_sent to only include hours and minutes
            time_sent_formatted = now.strftime('%I:%M')


            # Sender's chat with 'sent' status
            mychats, created = Mychats.objects.get_or_create(me=self.scope['user'], frnd=frnd)
            if created:
                mychats.chats = {}
                print(mychats.chats,"hhhhh")

            message_id = str(now) + "_sent"
            mychats.chats[message_id] = {
                'user': 'me',
                'msg': text_data['msg'],
                'status': 'unread',  # Initially marked as unread
                'time_sent': time_sent_formatted,
                'time_seen': None,
                'is_read': False  # Mark as not read
            }
            mychats.save()

            # Recipient's chat (also marked as unread)
            mychats, created = Mychats.objects.get_or_create(me=frnd, frnd=self.scope['user'])
            if created:
                mychats.chats = {}

            mychats.chats[message_id] = {
                'user': frnd.username,
                'msg': text_data['msg'],
                'status': 'unread',  # Marked unread for recipient
                'time_sent': time_sent_formatted,
                'time_seen': None,
                'is_read': False  # Mark as not read
            }
            mychats.save()

        except User.DoesNotExist:
            print(f"User {text_data['user']} not found.")

    async def send_videonotification(self, event):
        await self.send(event['msg'])

    # Add this method to your MychatApp class
    async def get_last_message(self, user):
        try:
            mychats = await database_sync_to_async(Mychats.objects.filter)(me=self.scope['user'], frnd=user)
            if mychats.exists():
                last_message = mychats.last().chats  # Get the last chat entry
                last_msg_key = list(last_message.keys())[-1]  # Get the last message key
                return last_message[last_msg_key]
        except Exception as e:
            print(f"Error retrieving last message: {e}")
        return None

    async def send_msg(self, event):
        print(f"Sending message: {event['msg']}")
        last_message = await self.get_last_message(event['sender'])
        await self.send(text_data=json.dumps({
            'msg': event['msg'],
            'sender': event['sender'],
            'last_msg': last_message['msg'] if last_message else None,
            'time_sent': last_message['time_sent'] if last_message else None,
            
        }))

    async def mark_as_read(self, message_id, recipient):
        """
        Marks the message as 'read' when the recipient opens the chat or acknowledges receipt.
        """
        await self.update_message_status(message_id, recipient, 'read')

    @database_sync_to_async
    def update_message_status(self, message_id, user, status):
        """
        Updates the status of the message (e.g., unread -> read) in the database.
        """
        try:
                # Update the message status in both sender's and recipient's chats
                mychats = Mychats.objects.filter(me=user).first()
                if mychats and message_id in mychats.chats:
                    mychats.chats[message_id]['status'] = status
                    mychats.chats[message_id]['is_read'] = (status == 'read')
                    if status == 'read':
                        mychats.chats[message_id]['time_seen'] = datetime.datetime.now().isoformat()
                    mychats.save()

        except Mychats.DoesNotExist:
                print(f"Chat not found for user {user}.")

    async def mark_as_read_handler(self, text_data):
        """
        Called when the recipient opens the chat or views the message.
        """
        data = json.loads(text_data)
        message_id = data.get('message_id')
        user = self.scope['user']

        # Mark the message as read
        if message_id:
            await self.mark_as_read(message_id, user)

from django.http import JsonResponse

def get_chat_history(request):
    user = request.GET.get('user')
    # Fetch messages from Mychats model
    chat_history = Mychats.objects.filter(me=request.user, frnd=user).first()
    
    if chat_history:
        messages = [
            {
                'user': message['user'],
                'msg': message['msg'],
                'time_sent': message['time_sent'],
                'isSent': message['status'] == 'sent',
            }
            for message in chat_history.chats.values()
        ]
        return JsonResponse(messages, safe=False)
    return JsonResponse([], safe=False)
    
