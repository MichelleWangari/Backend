from django.urls import path
from .views import SignupView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import VerifyOTPView
from .views import RoleUpdateView
from .views import RoleBasedDashboard
from .views import CustomTokenObtainPairView
from .views import ContactSubmissionCreateView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('contact/', ContactSubmissionCreateView.as_view(), name='contact-submission'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/<int:pk>/update-role/', RoleUpdateView.as_view(), name='update-role'),
    path('dashboard/', RoleBasedDashboard.as_view(), name='role-dashboard'), 
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
]
