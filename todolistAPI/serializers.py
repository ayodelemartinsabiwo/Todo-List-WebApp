from rest_framework import serializers
from .models import Users



class UsersSerializer(serializers.Serializer):
    models = Users
    fields = "__all__"
