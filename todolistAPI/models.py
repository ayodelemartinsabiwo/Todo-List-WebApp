from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.forms import ModelForm
from django.contrib.auth.models import User

# Create your models here.

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateTimeField()
    completed = models.BooleanField()
    important = models.BooleanField(default=False) #new field to store importance of task/status

    def __str__(self):
        return f"{self.user.id} - {self.title} - {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    #dunder name/string
    def __str__(self) -> str:
        return self.user.username
