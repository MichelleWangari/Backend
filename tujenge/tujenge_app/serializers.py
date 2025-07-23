# chama_app/serializers.py
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import AuthenticationFailed
from datetime import timedelta
from django.utils import timezone

from rest_framework import serializers
from django.utils import timezone
import random
from .models import User, ContactSubmission  # adjust the import as needed

class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
     
        otp = str(random.randint(100000, 999999))


        validated_data['otp'] = otp
        validated_data['otp_created_at'] = timezone.now()

    
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password'],
            otp=validated_data['otp'],
            otp_created_at=validated_data['otp_created_at']
        )

    
        print(f"OTP for {user.email} is: {otp}")

        return user


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

from rest_framework import serializers
from .models import ContactSubmission

class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ['name', 'email', 'subject', 'message']
        extra_kwargs = {
            'name': {'required': True},
            'email': {'required': True},
            'message': {'required': True}
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required")
        return value