from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


class Chat(models.Model):
    chat_id = models.CharField(max_length=36, unique=True, default=uuid4)
    chat_name = models.CharField(max_length=128, null=True, blank=True)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.chat_id


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name="chat_messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}-{self.chat.chat_id} : {self.content}"

    class Meta:
        ordering = ["-timestamp"]
