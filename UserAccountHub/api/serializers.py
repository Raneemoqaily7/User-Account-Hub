from rest_framework import serializers
from UserAccountHub.models import User,Account

class UserSerializer (serializers.ModelSerializer):
    class Meta :
        model = User
        fields ="__all__"
