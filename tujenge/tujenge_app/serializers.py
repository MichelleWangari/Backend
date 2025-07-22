# chama_app/serializers.py
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import AuthenticationFailed

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['role'] = user.role
        token['email'] = user.email
        return token

    def validate(self, attrs):
       
        attrs['username'] = attrs.get('email')

        data = super().validate(attrs)

        
        if not self.user.is_verified:
            raise AuthenticationFailed("Please verify your account with the OTP sent to your email.")

        return data

class OTPVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User not found.")

        if user.is_verified:
            raise serializers.ValidationError("User already verified.")

        if user.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        expiration_time = user.otp_created_at + timedelta(minutes=10)
        if timezone.now() > expiration_time:
            raise serializers.ValidationError("OTP has expired.")

        data['user'] = user
        return data
    
class RoleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role']
