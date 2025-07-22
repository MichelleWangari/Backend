from django.urls import path
from .views import SignupView
from .views import CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import VerifyOTPView
from .views import RoleUpdateView
from .views import RoleBasedDashboard


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('users/<int:pk>/update-role/', RoleUpdateView.as_view(), name='update-role'),
     path('dashboard/', RoleBasedDashboard.as_view(), name='role-dashboard'),
    
]
