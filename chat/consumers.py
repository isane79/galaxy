from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
import json
from .models import Message, Chat
from django.template.loader import render_to_string


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.default_chatroom_name = str(self.user.id)

        async_to_sync(self.channel_layer.group_add)(
            self.default_chatroom_name, self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.default_chatroom_name, self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        if text_data_json.get("type") == "switch_chat":
            self.handle_switch(text_data_json)
        else:
            self.handle_message(text_data_json)

    def handle_switch(self, text_data_json):
        new_chatroom_name = text_data_json["new_chatroom_name"]

        async_to_sync(self.channel_layer.group_discard)(
            self.default_chatroom_name, self.channel_name
        )
        async_to_sync(self.channel_layer.group_add)(
            new_chatroom_name, self.channel_name
        )

        self.default_chatroom_name = new_chatroom_name

        chat_group = get_object_or_404(Chat, chat_id=new_chatroom_name)
        html = render_to_string(
            "chat/messages.html",
            context={"messages": chat_group.chat_messages.all(), "user": self.user},
        )

        self.send(text_data=json.dumps({"type": "message", "html": html}))

    def handle_message(self, text_data_json):
        content = text_data_json["content"]
        chatroom_name = text_data_json["chatroom_name"]

        message = Message.objects.create(
            content=content,
            sender=self.user,
            chat=get_object_or_404(Chat, chat_id=chatroom_name),
        )
        event = {
            "type": "message_handler",
            "message_id": message.id,
            "chatroom_name": chatroom_name,
        }
        async_to_sync(self.channel_layer.group_send)(chatroom_name, event)

    def message_handler(self, event):
        message_id = event["message_id"]
        chatroom_name = event["chatroom_name"]
        message = Message.objects.get(id=message_id)

        if chatroom_name == self.default_chatroom_name:
            html = render_to_string(
                "chat/messages.html",
                context={"messages": [message], "user": self.user},
            )
            self.send(text_data=json.dumps({"type": "message", "html": html}))
