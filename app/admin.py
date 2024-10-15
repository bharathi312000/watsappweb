
from django.contrib import admin
from .models import Mychats, Notification, UserProfile

admin.site.register(Mychats)
admin.site.register(UserProfile)
admin.site.register(Notification)
