from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer
from .models import User
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from .serializers import OTPVerificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework import generics
from .serializers import RoleUpdateSerializer
from rest_framework.permissions import BasePermission

# Create your views here.
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(f"OTP for {user.email} is: {user.otp}")
            otp = get_random_string(length=6, allowed_chars='0123456789')
            user.otp = otp
            user.otp_created_at = timezone.now()
            user.save()
 
            return Response({"message": "User created. OTP sent to email."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.is_verified = True
            
            user.otp = None  
            user.otp_created_at = None
            user.save()
            return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class RoleUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = RoleUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class RoleBasedDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == 'admin':
            return Response({"message": "Welcome Admin!"})
        elif request.user.role == 'treasurer':
            return Response({"message": "Welcome Treasurer!"})
        elif request.user.role == 'member':
            return Response({"message": "Welcome Member!"})
        else:
            return Response({"error": "Unauthorized"}, status=403)
