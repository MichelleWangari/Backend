from django.urls import path
from .views import SignupView
from .views import CustomLoginView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
