from rest_framework import serializers
from UserAccountHub.models import User,Account

from django.contrib.auth.hashers import make_password

class UserSerializer (serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    gender = serializers.CharField(source='get_gender_display')
    class Meta :
        model = User
        fields ="__all__"
        depth = 1

class AccountSerializer(serializers.ModelSerializer):
    class Meta :
        model =Account
        fields ="__all__"


class Registerationerializer (serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ["email", "username", "password", "password2","firstName","lastName","status","gender","date_of_Birth"]
        extra_kwargs = {
            'password': {'write_only': True}
        }



    def save(self):
          
        email = self.validated_data["email"]
        username = self.validated_data["username"]
        password = self.validated_data["password"]
        password2 = self.validated_data["password2"]
        firstName = self.validated_data["firstName"]
        lastName=self.validated_data["lastName"]
        gender=self.validated_data["gender"]
        status=self.validated_data["status"]
        date_of_Birth=self.validated_data["date_of_Birth"]
        if password2 != password:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        
        user = User(email=email,firstName=firstName, username=username, password=make_password(password),date_of_Birth=date_of_Birth,lastName =lastName,gender=gender,status=status)
        user.save()
        return user
        
