from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='profile', on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # Stores the profile pic

    def __str__(self):
        return f"{self.user.username} Profile"
class Mychats(models.Model):
    me = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='it_me')
    frnd = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='my_frnd')
    chats = models.JSONField(default=dict)
    is_read = models.BooleanField(default=False) 

    def __str__(self):
        return f"{self.me}"
    

    
# Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User receiving the notification
    message = models.TextField()  # The notification message
    is_read = models.BooleanField(default=False)  # Track if the notification is read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"






