from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        #user create_user instead of manually settings password
        user = get_user_model().objects.create_user(**validated_data)
        
        #create token for the user
        
        Token.objects.create(user=user)
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password = attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs['user'] = user
        return attrs

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['bio', 'profile_picture']    
