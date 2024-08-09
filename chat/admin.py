from django.contrib import admin
from .models import Profile, Chat, Message

admin.site.register([Chat, Message, Profile])
